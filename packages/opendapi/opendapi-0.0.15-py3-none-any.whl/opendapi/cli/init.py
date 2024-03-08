"""Entrypoint for the OpenDAPI CLI `opendapi init` command."""
import os
from typing import List

import click

from jinja2 import Template

from opendapi.cli.common import check_command_invocation_in_root
from opendapi.config import SUPPORTED_DAPI_INTEGRATIONS
from opendapi.defs import (
    CONFIG_FILEPATH_FROM_ROOT_DIR,
    DEFAULT_DAPIS_DIR,
    DEFAULT_DAPI_SERVER_HOSTNAME,
    GITHUB_ACTIONS_FILEPATH_FROM_ROOT_DIR,
)
from opendapi.utils import make_snake_case, get_repo_name_from_root_dir

GITHUB_ACTIONS_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "github_actions.yaml.jinja"
)
OPENDAPI_CONFIG_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "opendapi.config.yaml.jinja"
)
TEAMS_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "teams.yaml.jinja"
)
DATASTORES_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "datastores.yaml.jinja"
)


def _read_template_file(template_path: str) -> str:
    """Read the contents of the template file."""
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def _render_template(output_filepath: str, template_path: str, template_input: dict):
    """Render the template and write it to the output file."""

    template_content = _read_template_file(template_path)
    if not os.path.exists(os.path.dirname(output_filepath)):
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as file:
        template = Template(template_content, autoescape=True)
        file.write(template.render(**template_input))


def _create_from_template(
    config_name: str,
    write_filepath: str,
    template_filepath: str,
    force_recreate: bool,
    template_input: dict,
):
    """Create the .github/workflows/opendapi_ci.yml file."""
    click.secho(
        f"\nCreating the {config_name}...",
        fg="yellow",
    )
    if not force_recreate and os.path.isfile(write_filepath):
        click.secho(
            f"  The {config_name} file at {write_filepath} already exists. "
            "Set force_recreate to true to recreate it. Skipping now...",
            fg="red",
        )
        return

    _render_template(
        write_filepath,
        template_filepath,
        template_input,
    )

    click.secho(
        f"  Done creating {write_filepath}",
        fg="green",
    )


def _prompt_for_integrations() -> List[str]:
    """Prompt the user for the integrations they want to use."""
    click.echo(
        "Enter the integrations you want to use with OpenDAPI in this repository (empty to finish)"
        " - you can add more or update later."
    )
    integrations = []
    while True:
        value = click.prompt(
            "  Integration name",
            type=click.Choice([""] + list(SUPPORTED_DAPI_INTEGRATIONS)),
            default="",
            show_default=False,
        )
        if not value.strip() and integrations:
            break
        if value:
            integrations.append(value.strip())

    return integrations


@click.command()
@click.option(
    "--org-name",
    type=str,
    help="The name of the organization that owns the data.",
    prompt="Enter your organization name",
)
@click.option(
    "--org-email-domain",
    type=str,
    help="The email domain of the organization that owns the data.",
    prompt="Enter your organization email domain",
)
@click.option(
    "--mainline-branch-name",
    type=str,
    default="main",
    help="The name of the mainline branch in this Git repository.",
    prompt="Enter the name of the mainline branch of this Git repository",
)
@click.option(
    "--force-recreate",
    is_flag=True,
    help="Recreate the OpenDAPI configuration files if true, otherwise skip.",
    default=False,
)
def cli(
    org_name: str,
    org_email_domain: str,
    mainline_branch_name: str,
    force_recreate: bool,
):
    """
    Initializes OpenDAPI in this Github repository.
    """
    click.secho(
        f"\nWelcome to OpenDAPI, {org_name}!"
        " This command will help you set up OpenDAPI in your repository.",
        fg="green",
    )

    root_dir = os.getcwd()
    org_name_snakecase = make_snake_case(org_name)
    repo_name = get_repo_name_from_root_dir(root_dir)

    click.secho(
        "\n\nStep 1: Let us check some things before we proceed...", fg="yellow"
    )
    check_command_invocation_in_root()

    integrations = _prompt_for_integrations()

    click.secho("\n\nStep 2: Creating necessary files from templates...", fg="yellow")
    _create_from_template(
        "OpenDAPI configuration file",
        os.path.join(root_dir, CONFIG_FILEPATH_FROM_ROOT_DIR),
        OPENDAPI_CONFIG_TEMPLATE_PATH,
        force_recreate,
        {
            "org_name": org_name,
            "org_name_snakecase": org_name_snakecase,
            "org_email_domain": org_email_domain,
            "mainline_branch_name": mainline_branch_name,
            "repo_name": repo_name,
            "include_activerecord": "activerecord" in integrations,
            "include_dbt": "dbt" in integrations,
            "include_pynamodb": "pynamodb" in integrations,
            "include_sqlalchemy": "sqlalchemy" in integrations,
        },
    )

    _create_from_template(
        "GitHub Actions CI file",
        os.path.join(root_dir, GITHUB_ACTIONS_FILEPATH_FROM_ROOT_DIR),
        GITHUB_ACTIONS_TEMPLATE_PATH,
        force_recreate,
        {
            "org_name": org_name,
            "org_email_domain": org_email_domain,
            "mainline_branch_name": mainline_branch_name,
            "dapi_server_hostname": DEFAULT_DAPI_SERVER_HOSTNAME,
        },
    )

    _create_from_template(
        "Teams registry file",
        os.path.join(root_dir, DEFAULT_DAPIS_DIR, f"{org_name_snakecase}.teams.yaml"),
        TEAMS_TEMPLATE_PATH,
        force_recreate,
        {
            "org_name": org_name,
            "org_name_snakecase": org_name_snakecase,
            "org_email_domain": org_email_domain,
        },
    )

    _create_from_template(
        "Datastores registry file",
        os.path.join(
            root_dir, DEFAULT_DAPIS_DIR, f"{org_name_snakecase}.datastores.yaml"
        ),
        DATASTORES_TEMPLATE_PATH,
        force_recreate,
        {
            "org_name": org_name,
            "org_name_snakecase": org_name_snakecase,
        },
    )

    click.secho(
        "\n\nStep 3: Please review & modify the following files to ensure sucessful installation:\n"
        f"  a. {os.path.join(DEFAULT_DAPIS_DIR, f'{org_name_snakecase}.teams.yaml')} "
        "has the teams for assigning data ownership with ways to reach them\n"
        f"  b. {os.path.join(DEFAULT_DAPIS_DIR, f'{org_name_snakecase}.datastores.yaml')} "
        "has the datastores used for impact analysis with host/credential information\n"
        f"  c. {CONFIG_FILEPATH_FROM_ROOT_DIR} "
        "has the ORM integration configuration and playbooks"
        " to assign team ownership and datastore object names\n"
        f"  d. {GITHUB_ACTIONS_FILEPATH_FROM_ROOT_DIR} "
        "has the Github actions to interact with the DAPI servers for AI-driven DAPI generation\n",
        fg="yellow",
    )

    click.secho(
        "OpenDAPI has been initialized in your repository.\n"
        "Please commit and spin up a PR (or do opendapi run) to see the magic happen!\n",
        fg="green",
    )
