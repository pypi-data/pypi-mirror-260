import ast
import os
import re
import subprocess
import sys
import time
from typing import Optional

import click
import inquirer
import inquirer.themes
import tomlkit
from git import Repo

from codeflash.analytics.posthog import ph
from codeflash.code_utils.env_utils import (
    get_codeflash_api_key,
    read_api_key_from_shell_config,
    SHELL_RC_EXPORT_PATTERN,
)
from codeflash.code_utils.env_utils import get_shell_rc_path
from codeflash.code_utils.git_utils import get_github_secrets_page_url
from codeflash.version import __version__ as version

CODEFLASH_LOGO: str = (
    "\n"
    r"              __    _____         __ " + "\n"
    r" _______  ___/ /__ / _/ /__ ____ / / " + "\n"
    r"/ __/ _ \/ _  / -_) _/ / _ `(_-</ _ \ " + "\n"
    r"\__/\___/\_,_/\__/_//_/\_,_/___/_//_/" + "\n"
    f"{('v'+version).rjust(46)}\n"
    "                          https://codeflash.ai\n"
    "\n"
)


def init_codeflash():
    click.echo(CODEFLASH_LOGO)
    click.echo("⚡️ Welcome to CodeFlash! Let's get you set up.\n")

    did_add_new_key = prompt_api_key()

    setup_info: dict[str, str] = {}

    collect_setup_info(setup_info)

    configure_pyproject_toml(setup_info)

    prompt_github_action(setup_info)

    ask_run_end_to_end_test(setup_info)  # mebbe run this after the following help text?

    click.echo(
        "\n"
        "⚡️ CodeFlash is now set up! You can now run:\n"
        "    codeflash --file <path-to-file> --function <function-name> to optimize a function within a file\n"
        "    codeflash --file <path-to-file> to optimize all functions in a file\n"
        f"    codeflash --all to optimize all functions in all files in the module you selected ({setup_info['module_root']})\n"
        # "    codeflash --pr <pr-number> to optimize a PR\n"
        "-or-\n"
        "    codeflash --help to see all options\n"
    )
    if did_add_new_key:
        click.echo(
            "🐚 Don't forget to restart your shell to load the CODEFLASH_API_KEY environment variable!"
        )
        click.echo("Or run the following command to reload:")
        click.echo(f"  source {get_shell_rc_path()}")

    ph("cli-installation-successful", {"did_add_new_key": did_add_new_key})


def ask_run_end_to_end_test(setup_info):
    run_tests_answer = inquirer.prompt(
        [
            inquirer.Confirm(
                "run_tests",
                message="⚡️ Do you want to run a sample optimization to make sure everything's set up correctly? (takes about 3 minutes)",
                default=True,
            )
        ]
    )
    run_tests = run_tests_answer.get("run_tests", False)
    if run_tests:
        create_bubble_sort_file(setup_info)
        run_end_to_end_test(setup_info)


def collect_setup_info(setup_info: dict[str, str]):
    curdir = os.getcwd()
    # Check if the cwd is writable
    if not os.access(curdir, os.W_OK):
        click.echo(
            f"❌ The current directory isn't writable, please check your folder permissions and try again.\n"
        )
        click.echo("It's likely you don't have write permissions for this folder.")
        sys.exit(1)

    # Check for the existence of pyproject.toml or setup.py
    project_name = check_for_toml_or_setup_file()

    ignore_subdirs = [
        "venv",
        "node_modules",
        "dist",
        "build",
        "build_temp",
        "build_scripts",
        "env",
        "logs",
        "tmp",
    ]
    valid_subdirs = [
        d
        for d in next(os.walk("."))[1]
        if not d.startswith(".") and not d.startswith("__") and d not in ignore_subdirs
    ]

    valid_module_subdirs = [dir for dir in valid_subdirs if dir != "tests"]

    curdir_option = "current directory (" + curdir + ")"
    module_subdir_options = valid_module_subdirs + [curdir_option]

    module_root_answer = inquirer.prompt(
        [
            inquirer.List(
                "module_root",
                message="Which Python module do you want me to optimize going forward?\n"
                + "(This is usually the top-most directory where all your Python source code is located)",
                choices=module_subdir_options,
                default=(
                    project_name
                    if project_name in module_subdir_options
                    else module_subdir_options[0]
                ),
            )
        ]
    )
    module_root = module_root_answer["module_root"]
    setup_info["module_root"] = "." if module_root == curdir_option else module_root
    ph("cli-project-root-provided")

    # Discover test directory
    default_tests_subdir = "tests"
    create_for_me_option = "okay, create a tests/ directory for me!"
    test_subdir_options = valid_subdirs if len(valid_subdirs) > 0 else [create_for_me_option]
    custom_dir_option = "enter a custom directory..."
    test_subdir_options.append(custom_dir_option)
    tests_root_answer = inquirer.prompt(
        [
            inquirer.List(
                "tests_root",
                message="Where are your tests located? "
                "(If you don't have any tests yet, I can create an empty tests/ directory for you)",
                choices=test_subdir_options,
                default=(
                    default_tests_subdir
                    if default_tests_subdir in test_subdir_options
                    else test_subdir_options[0]
                ),
            )
        ]
    )
    tests_root = tests_root_answer["tests_root"]
    if tests_root == create_for_me_option:
        tests_root = os.path.join(curdir, default_tests_subdir)
        os.mkdir(tests_root)
        click.echo(f"✅ Created directory {tests_root}/\n")
    elif tests_root == custom_dir_option:
        custom_tests_root_answer = inquirer.prompt(
            [
                inquirer.Path(
                    "custom_tests_root",  # Removed the colon and space from the message
                    message=f"Enter the path to your tests directory inside {os.path.abspath(module_root) + os.sep} ",
                    path_type=inquirer.Path.DIRECTORY,
                    exists=True,
                    normalize_to_absolute_path=True,
                ),
            ]
        )
        tests_root = custom_tests_root_answer["custom_tests_root"]
    setup_info["tests_root"] = os.path.relpath(tests_root, curdir)
    ph("cli-tests-root-provided")

    # Autodiscover test framework
    test_framework = detect_test_framework(curdir, tests_root)
    autodetected = f" (seems to me you're using {test_framework})" if test_framework else ""
    questions = [
        inquirer.List(
            "test_framework",
            message="Which test framework do you use?" + autodetected,
            choices=["pytest", "unittest"],
            default=test_framework or "pytest",
            carousel=True,
        )
    ]
    answers = inquirer.prompt(questions)
    setup_info["test_framework"] = answers["test_framework"]

    ph("cli-test-framework-provided", {"test_framework": setup_info["test_framework"]})

    # Ask for paths to ignore and update the setup_info dictionary
    # ignore_paths_input = click.prompt("Are there any paths CodeFlash should ignore? (comma-separated, no spaces)",
    #                                   default='', show_default=False)
    # ignore_paths = ignore_paths_input.split(',') if ignore_paths_input else ['tests/']
    ignore_paths = []
    setup_info["ignore_paths"] = ignore_paths

    # Ask the user if they agree to enable PostHog analytics logging
    # enable_analytics_question = [
    #     inquirer.List(
    #         "enable_analytics",
    #         message="⚡️ Is it OK to collect usage analytics to help improve CodeFlash? (recommended)",
    #         choices=[
    #             ("Sure, I'd love to help make CodeFlash better!", True),
    #             ("No, thanks.", False),
    #         ],
    #     )
    # ]
    # enable_analytics_answer = inquirer.prompt(enable_analytics_question)
    # setup_info["enable_analytics"] = enable_analytics_answer["enable_analytics"]

    ph("cli-analytics-choice", {"enable_analytics": setup_info["enable_analytics"]})


def detect_test_framework(curdir, tests_root) -> Optional[str]:
    test_framework = None
    pytest_files = ["pytest.ini", "pyproject.toml", "tox.ini", "setup.cfg"]
    pytest_config_patterns = {
        "pytest.ini": "[pytest]",
        "pyproject.toml": "[tool.pytest.ini_options]",
        "tox.ini": "[pytest]",
        "setup.cfg": "[tool:pytest]",
    }
    for pytest_file in pytest_files:
        file_path = os.path.join(curdir, pytest_file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf8") as file:
                contents = file.read()
                if pytest_config_patterns[pytest_file] in contents:
                    test_framework = "pytest"
                    break
        test_framework = "pytest"
    else:
        # Check if any python files contain a class that inherits from unittest.TestCase
        for filename in os.listdir(tests_root):
            if filename.endswith(".py"):
                with open(os.path.join(tests_root, filename), "r", encoding="utf8") as file:
                    contents = file.read()
                    try:
                        node = ast.parse(contents)
                    except SyntaxError:
                        continue
                    if any(
                        isinstance(item, ast.ClassDef)
                        and any(
                            isinstance(base, ast.Attribute)
                            and base.attr == "TestCase"
                            or isinstance(base, ast.Name)
                            and base.id == "TestCase"
                            for base in item.bases
                        )
                        for item in node.body
                    ):
                        test_framework = "unittest"
                        break
    return test_framework


def check_for_toml_or_setup_file() -> Optional[str]:
    click.echo()
    click.echo("Checking for pyproject.toml or setup.py ...\r", nl=False)
    curdir = os.getcwd()
    pyproject_toml_path = os.path.join(curdir, "pyproject.toml")
    setup_py_path = os.path.join(curdir, "setup.py")
    project_name = None
    if os.path.exists(pyproject_toml_path):
        try:
            with open(pyproject_toml_path, "r", encoding="utf8") as f:
                pyproject_toml_content = f.read()
            project_name = tomlkit.parse(pyproject_toml_content)["tool"]["poetry"]["name"]
            click.echo(f"✅ I found a pyproject.toml for your project {project_name}.")
            ph("cli-pyproject-toml-found-name")
        except Exception as e:
            click.echo(f"✅ I found a pyproject.toml for your project.")
            ph("cli-pyproject-toml-found")
    elif os.path.exists(setup_py_path):
        with open(setup_py_path, "r", encoding="utf8") as f:
            setup_py_content = f.read()
        project_name_match = re.search(
            r"setup\s*\([^)]*?name\s*=\s*['\"](.*?)['\"]", setup_py_content, re.DOTALL
        )
        if project_name_match:
            project_name = project_name_match.group(1)
            click.echo(f"✅ Found setup.py for your project {project_name}")
            ph("cli-setup-py-found-name")
        else:
            click.echo(f"✅ Found setup.py.")
            ph("cli-setup-py-found")
    else:
        click.echo(
            f"💡 I couldn't find a pyproject.toml in the current directory ({curdir}).\n"
            "(make sure you're running `codeflash init` from your project's root directory!)\n"
            f"I need this file to store my configuration settings."
        )
        ph("cli-no-pyproject-toml-or-setup-py")

        # Create a pyproject.toml file because it doesn't exist
        create_toml = inquirer.confirm(
            f"Do you want me to create a pyproject.toml file in the current directory?",
            default=True,
            show_default=False,
        )
        if create_toml:
            ph("cli-create-pyproject-toml")
            # Define a minimal pyproject.toml content
            new_pyproject_toml = tomlkit.document()
            new_pyproject_toml["tool"] = {"codeflash": {}}
            try:
                with open(pyproject_toml_path, "w", encoding="utf8") as pyproject_file:
                    pyproject_file.write(tomlkit.dumps(new_pyproject_toml))

                # Check if the pyproject.toml file was created
                if os.path.exists(pyproject_toml_path):
                    click.echo(f"✅ Created a pyproject.toml file at {pyproject_toml_path}")
                    click.pause()
                ph("cli-created-pyproject-toml")
            except IOError as e:
                click.echo(
                    "❌ Failed to create pyproject.toml. Please check your disk permissions and available space."
                )
                apologize_and_exit()
        else:
            click.echo("⏩️ Skipping pyproject.toml creation.")
            apologize_and_exit()
    click.echo()
    return project_name


def apologize_and_exit():
    click.echo(
        "💡 If you're having trouble, see https://app.codeflash.ai/app/getting-started for further help getting started with CodeFlash!"
    )
    click.echo("Exiting...")
    sys.exit(1)


# Ask if the user wants CodeFlash to optimize new GitHub PRs
def prompt_github_action(setup_info: dict[str, str]):
    optimize_prs_answer = inquirer.prompt(
        [
            inquirer.Confirm(
                "optimize_prs",
                message="Do you want CodeFlash to automatically optimize new Github PRs when they're opened (recommended)?",
                default=True,
            )
        ]
    )
    optimize_yes = optimize_prs_answer["optimize_prs"]
    ph("cli-github-optimization-choice", {"optimize_prs": optimize_yes})
    if optimize_yes:
        repo = Repo(setup_info["module_root"], search_parent_directories=True)
        git_root = repo.git.rev_parse("--show-toplevel")
        workflows_path = os.path.join(git_root, ".github", "workflows")
        optimize_yaml_path = os.path.join(workflows_path, "codeflash-optimize.yaml")

        confirm_creation_answer = inquirer.prompt(
            [
                inquirer.Confirm(
                    "confirm_creation",
                    message=f"Great! I'll create a new workflow file at {optimize_yaml_path} ... is this OK?",
                    default=True,
                )
            ]
        )
        confirm_creation_yes = confirm_creation_answer["confirm_creation"]
        ph(
            "cli-github-optimization-confirm-workflow-creation",
            {"confirm_creation": confirm_creation_yes},
        )
        if confirm_creation_yes:
            os.makedirs(workflows_path, exist_ok=True)
            from importlib.resources import read_text

            py_version = sys.version_info
            python_version_string = f" {py_version.major}.{py_version.minor}"

            optimize_yml_content = read_text(
                "codeflash.cli_cmds.workflows", "codeflash-optimize.yaml"
            )
            optimize_yml_content = optimize_yml_content.replace(
                " {{ python_version }}", python_version_string
            )
            with open(optimize_yaml_path, "w", encoding="utf8") as optimize_yml_file:
                optimize_yml_file.write(optimize_yml_content)
            click.echo(f"✅ Created {optimize_yaml_path}\n")
            click.prompt(
                f"Next, you'll need to add your CODEFLASH_API_KEY as a secret to your GitHub repo.\n"
                + f"Press Enter to open your repo's secrets page at {get_github_secrets_page_url(repo)} ...\n"
                + f"Then, click 'New repository secret' to add your api key with the variable name CODEFLASH_API_KEY.\n",
                default="",
                type=click.STRING,
                prompt_suffix="",
                show_default=False,
            )
            click.launch(get_github_secrets_page_url(repo))
            click.echo(
                "🐙 I opened your Github secrets page! Note: if you see a 404, you probably don't have access to this "
                + "repo's secrets; ask a repo admin to add it for you, or (not super recommended) you can temporarily "
                "hard-code your api key into the workflow file.\n",
            )
            click.pause()
            click.echo()
            click.prompt(
                f"Finally, for the workflow to work, you'll need to edit the workflow file to install the right "
                f"Python version and any project dependencies.\n"
                + f"Press Enter to open {optimize_yaml_path} in your editor.\n",
                default="",
                type=click.STRING,
                prompt_suffix="",
                show_default=False,
            )
            click.launch(optimize_yaml_path)
            click.echo(
                "📝 I opened the workflow file in your editor! You'll need to edit the steps that install the right Python "
                + "version and any project dependencies. See the comments in the file for more details.\n"
            )
            click.pause()
            click.echo()
            click.echo("🚀 CodeFlash is now configured to automatically optimize new Github PRs!\n")
            ph("cli-github-workflow-created")
        else:
            click.echo("⏩️ Skipping GitHub workflow creation.")
            ph("cli-github-workflow-skipped")


# Create or update the pyproject.toml file with the CodeFlash dependency & configuration
def configure_pyproject_toml(setup_info: dict[str, str]):
    toml_path = os.path.join(os.getcwd(), "pyproject.toml")
    try:
        with open(toml_path, "r", encoding="utf8") as pyproject_file:
            pyproject_data = tomlkit.parse(pyproject_file.read())
    except FileNotFoundError:
        click.echo(
            f"I couln't find a pyproject.toml in the current directory.\n"
            f"Please create it by running `poetry init`, or run `codeflash init` again from a different project directory."
        )
        apologize_and_exit()

    codeflash_section = tomlkit.table()
    codeflash_section["module-root"] = setup_info["module_root"]
    codeflash_section["tests-root"] = setup_info["tests_root"]
    codeflash_section["test-framework"] = setup_info["test_framework"]
    codeflash_section["ignore-paths"] = setup_info["ignore_paths"]
    codeflash_section["enable-analytics"] = setup_info["enable_analytics"]

    # Add the 'codeflash' section, ensuring 'tool' section exists
    tool_section = pyproject_data.get("tool", tomlkit.table())
    tool_section["codeflash"] = codeflash_section
    pyproject_data["tool"] = tool_section

    click.echo(f"Writing CodeFlash configuration ...\r", nl=False)
    with open(toml_path, "w", encoding="utf8") as pyproject_file:
        pyproject_file.write(tomlkit.dumps(pyproject_data))
    click.echo(f"✅ Added CodeFlash configuration to {toml_path}")
    click.echo()


class CFAPIKeyType(click.ParamType):
    name = "cfapi-key"

    def convert(self, value, param, ctx):
        value = value.strip()
        if value.startswith("cf-") or value == "":
            return value
        else:
            self.fail(
                f"That key [{value}] seems to be invalid. It should start with a 'cf-' prefix. Please try again.",
                param,
                ctx,
            )


# Returns True if the user entered a new API key, False if they used an existing one
def prompt_api_key() -> bool:
    try:
        existing_api_key = get_codeflash_api_key()
    except EnvironmentError:
        existing_api_key = None
    if existing_api_key:
        display_key = f"{existing_api_key[:3]}****{existing_api_key[-4:]}"
        click.echo(f"🔑 I found a CODEFLASH_API_KEY in your environment [{display_key}]!")

        use_existing_key = inquirer.confirm(
            message="Do you want to use this key?",
            default=True,
            show_default=False,
        )
        if use_existing_key:
            ph("cli-existing-api-key-used")
            return False

    enter_api_key_and_save_to_rc()
    ph("cli-new-api-key-entered")
    return True


def enter_api_key_and_save_to_rc():
    browser_launched = False
    api_key = ""
    while api_key == "":
        api_key = click.prompt(
            f"Enter your CodeFlash API key{' [or press Enter to open your API key page]' if not browser_launched else ''}",
            hide_input=False,
            default="",
            type=CFAPIKeyType(),
            show_default=False,
        ).strip()
        if api_key:
            break
        else:
            if not browser_launched:
                click.echo(
                    "Opening your CodeFlash API key page. Grab a key from there!\n"
                    "You can also open this link manually: https://app.codeflash.ai/app/apikeys"
                )
                click.launch("https://app.codeflash.ai/app/apikeys")
                browser_launched = True  # This does not work on remote consoles

    shell_rc_path = get_shell_rc_path()
    api_key_line = f"export CODEFLASH_API_KEY={api_key}"
    try:
        with open(shell_rc_path, "r+", encoding="utf8") as shell_file:
            shell_contents = shell_file.read()
            existing_api_key = read_api_key_from_shell_config()

            if existing_api_key:
                # Replace the existing API key line
                updated_shell_contents = re.sub(
                    SHELL_RC_EXPORT_PATTERN, api_key_line, shell_contents
                )
                action = "Updated CODEFLASH_API_KEY in"
            else:
                # Append the new API key line
                updated_shell_contents = shell_contents.rstrip() + f"\n{api_key_line}\n"
                action = "Added CODEFLASH_API_KEY to"

            shell_file.seek(0)
            shell_file.write(updated_shell_contents)
            shell_file.truncate()
        click.echo(f"✅ {action} {shell_rc_path}.")
    except IOError as e:
        click.echo(
            f"💡 I tried adding your CodeFlash API key to {shell_rc_path} - but seems like I don't have permissions to do so.\n"
            f"You'll need to open it yourself and add the following line:\n\n{api_key_line}\n"
        )
        click.pause()

    os.environ["CODEFLASH_API_KEY"] = api_key


def create_bubble_sort_file(setup_info: dict[str, str]):
    bubble_sort_content = """def sorter(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr
"""
    bubble_sort_path = os.path.join(setup_info["module_root"], "bubble_sort.py")
    with open(bubble_sort_path, "w", encoding="utf8") as bubble_sort_file:
        bubble_sort_file.write(bubble_sort_content)
    click.echo(f"✅ Created {bubble_sort_path}")


def run_end_to_end_test(setup_info: dict[str, str]):
    command = [
        "codeflash",
        "--file",
        "bubble_sort.py",
        "--function",
        "sorter",
    ]
    animation = "|/-\\"
    idx = 0
    sys.stdout.write("Running sample optimization... ")
    sys.stdout.flush()
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=setup_info["module_root"],
    )
    while process.poll() is None:
        sys.stdout.write(animation[idx % len(animation)])
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write("\b")
        idx += 1

    sys.stdout.write(" ")  # Clear the last animation character
    sys.stdout.flush()
    stderr = process.stderr.read()
    if stderr:
        click.echo(stderr.strip())

    bubble_sort_path = os.path.join(setup_info["module_root"], "bubble_sort.py")

    # Delete the bubble_sort.py file after the test
    os.remove(bubble_sort_path)
    click.echo(f"🗑️ Deleted {bubble_sort_path}")

    if process.returncode == 0:
        click.echo("\n✅ End-to-end test passed. CodeFlash has been correctly set up!")
    else:
        click.echo(
            "\n❌ End-to-end test failed. Please check the logs above, and take a look at https://app.codeflash.ai/app/getting-started for help and troubleshooting."
        )
