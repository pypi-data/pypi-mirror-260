"""Entrypoint for the OpenDAPI CLI `opendapi generate` command."""
import os
import click

from opendapi.cli.common import (
    check_command_invocation_in_root,
    pretty_print_errors,
    get_opendapi_config,
    check_if_opendapi_config_is_valid,
)
from opendapi.validators.base import MultiValidationError
from opendapi.validators.teams import TeamsValidator
from opendapi.validators.datastores import DatastoresValidator

from opendapi.validators.dapi import ActiveRecordDapiValidator, DbtDapiValidator


@click.command()
def cli():
    """
    Generate DAPI files for integrations specified in the OpenDAPI configuration file.

    For certain integrations such as DBT and PynamoDB, this command will also run
    additional commands in the respective integration directories to generate DAPI files.
    """
    click.secho(
        "\nHello, again!"
        " This command will use your `opendapi.config.yaml` configuration"
        " to generate DAPI files for your integrations.",
        fg="green",
    )
    click.secho("\n\nChecking if we are in the right repository...", fg="yellow")

    check_command_invocation_in_root()
    root_dir = os.getcwd()
    config = get_opendapi_config(root_dir)

    check_if_opendapi_config_is_valid(config)

    validators = [
        TeamsValidator,
        DatastoresValidator,
    ]

    click.secho("\n\nIdentifying your integrations...", fg="yellow")
    if config.has_integration("activerecord"):
        validators.append(ActiveRecordDapiValidator)
        click.secho("  Found Activerecord...", fg="green")

    if config.has_integration("dbt"):
        validators.append(DbtDapiValidator)
        click.secho("  Found DBT...", fg="green")

    if config.has_integration("pynamodb"):
        # add test case if lib is installed
        # try invoking the test case
        click.secho("  Found PynamoDB...", fg="green")

    if config.has_integration("sqlalchemy"):
        # add test case if lib is installed
        # try invoking the test case
        click.secho("  Found SqlAlchemy...", fg="green")

    click.secho("\n\nGenerating DAPIs for your integrations...", fg="yellow")
    errors = []
    for validator in validators:
        inst_validator = validator(
            root_dir=root_dir,
            enforce_existence=True,
            should_autoupdate=True,
        )

        try:
            inst_validator.run()
        except MultiValidationError as exc:
            errors.append(exc)
    if errors:
        pretty_print_errors(errors)
        raise click.ClickException("Encountered one or more validation errors")

    click.secho("\n\nSuccess!", fg="green", bold=True)
