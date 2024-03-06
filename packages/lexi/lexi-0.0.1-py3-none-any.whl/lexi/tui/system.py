import os
import subprocess
from getpass import getpass
from string import Template

import typer
from typer import Option

import lexi.settings as settings
from lexi.utils.rich_logger import RichLogger

system_folder_path = os.path.join(os.path.dirname(__file__), "../system")

logger = RichLogger("application.log")

system_app = typer.Typer()


@system_app.command("up")
def system_up(
    fail_on_no_openai_api_key: bool = Option(
        False,
        "--fail-on-no-openai-api-key",
        help="Fail if there is no OPENAI_API_KEY in the environment.",
    ),
):
    """
    Starts the Docker Compose services.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        message = "OPENAI_API_KEY is not set in the environment."
        if fail_on_no_openai_api_key:
            logger.log_error(message)
            raise typer.Exit(code=1)
        else:
            logger.log_warning(message)

    try:
        env = os.environ.copy()
        env["COMPOSE_PROJECT_NAME"] = settings.COMPOSE_PROJECT_NAME

        subprocess.run(
            ["docker-compose", "up", "-d"], check=True, cwd=system_folder_path, env=env
        )
        logger.log_success("Docker Compose services have been started.")
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Failed to start Docker Compose services: {e}")


@system_app.command("down")
def system_down():
    """
    Stops the Docker Compose services.
    """
    try:
        subprocess.run(["docker-compose", "down"], check=True, cwd=system_folder_path)
        logger.log_success("Docker Compose services have been stopped.")
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Failed to stop Docker Compose services: {e}")


def load_template(file_path: str) -> Template:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            template_content = file.read()
            return Template(template_content)
    except FileNotFoundError:
        logger.log_error(f"Template file {file_path} not found.")
        return None


@system_app.command("create_envrc")
def create_envrc(
    confluence_url: str = typer.Option(..., prompt=True),
    confluence_space_key: str = typer.Option(..., prompt=True),
    confluence_email: str = typer.Option(..., prompt=True),
    confluence_space_name: str = typer.Option("", prompt=True),
    compose_project_name: str = typer.Option(..., prompt=True),
    litellm_log: str = typer.Option("INFO", prompt=True),
    force: bool = Option(
        False, "--force", "-f", help="Force overwrite of existing .envrc file"
    ),
):
    """
    Creates a .envrc file with the specified environment variables.
    """
    envrc_file_path = ".envrc"

    # Check if .envrc file exists
    if os.path.exists(envrc_file_path) and not force:
        typer.echo("The .envrc file already exists. Use --force to overwrite.")
        raise typer.Exit()

    # Load the template from the file
    template = load_template(settings.ENVRC_TEMPLATE_FILE)

    confluence_api_key = getpass("Enter Confluence API Key: ")
    openai_api_key = getpass("Enter OpenAI API Key: ")

    # Substitute values in the template
    variables = {
        "confluence_private_api_key": confluence_api_key,
        "confluence_space_url": confluence_url,  # Make sure confluence_url is defined
        "confluence_space_key": confluence_space_key,  # Make sure confluence_space_key is defined
        "confluence_email_address": confluence_email,  # Make sure confluence_email is defined
        "confluence_space_name": confluence_space_name or "",
        "openai_api_key": openai_api_key,
        "compose_project_name": compose_project_name,  # Make sure compose_project_name is defined
        "litellm_log": litellm_log,  # Make sure litellm_log is defined
    }

    # Substitute the variables in the template
    envrc_content = template.substitute(variables)

    with open(".envrc", "w", encoding="utf-8") as f:
        f.write(envrc_content)

    logger.log_success("The .envrc file has been created successfully.")


if __name__ == "__main__":
    system_app()
