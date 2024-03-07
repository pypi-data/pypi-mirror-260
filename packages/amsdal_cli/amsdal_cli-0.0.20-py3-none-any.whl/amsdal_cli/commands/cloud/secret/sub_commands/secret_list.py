import json
from pathlib import Path
from typing import Annotated

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table

from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.commands.cloud.secret.app import secret_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@secret_sub_app.command(name='list')
def secret_list_command(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    values: Annotated[bool, typer.Option('--values', '-v', help='Show secret values')] = False,
) -> None:
    """
    List the app secrets on the Cloud Server.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        list_response = manager.cloud_actions_manager.list_secrets(
            with_values=values,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    if not list_response:
        return

    if output == OutputFormat.json:
        print(json.dumps(list_response.model_dump(), indent=4))
        return

    if not list_response.secrets:
        print('No secrets found.')
        return

    data_table = Table()
    data_table.add_column('Secret Name', justify='center')

    if values:
        data_table.add_column('Secret Value', justify='center')

    for secret in list_response.secrets:
        if values:
            secret_name, secret_value = secret.split('=', 1)
            data_table.add_row(secret_name, secret_value)
        else:
            data_table.add_row(secret)

    print(data_table)
