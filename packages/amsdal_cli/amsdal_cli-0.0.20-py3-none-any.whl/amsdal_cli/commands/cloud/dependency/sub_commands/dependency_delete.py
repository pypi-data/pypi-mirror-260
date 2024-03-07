from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.dependency.app import dependency_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@dependency_sub_app.command(name='delete')
def dependency_delete_command(
    ctx: typer.Context,
    dependency_name: str,
) -> None:
    """
    Delete dependency from your Cloud Server app.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.delete_dependency(
            dependency_name=dependency_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    print('[green]Dependency deleted successfully[/green]')
