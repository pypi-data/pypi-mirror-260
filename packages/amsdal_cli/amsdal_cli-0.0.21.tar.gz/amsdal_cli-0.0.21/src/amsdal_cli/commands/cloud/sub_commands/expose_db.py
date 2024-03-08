from pathlib import Path
from typing import Optional

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.app import cloud_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@cloud_sub_app.command(name='expose_db')
def expose_db_command(ctx: typer.Context, ip_address: Optional[str] = None) -> None:  # noqa: UP007
    """
    Add your IP to the whitelist of the database and return the connection configs.
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        response = manager.cloud_actions_manager.expose_db(
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            ip_address=ip_address,
        )
        print(response)
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return
