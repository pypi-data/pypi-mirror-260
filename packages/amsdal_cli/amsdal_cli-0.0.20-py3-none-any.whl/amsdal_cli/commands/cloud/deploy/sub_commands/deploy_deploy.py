from pathlib import Path

import typer
from amsdal.cloud.enums import DeployType
from amsdal.cloud.enums import LakehouseOption
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@deploy_sub_app.callback(invoke_without_command=True)
def deploy_command(
    ctx: typer.Context,
    deploy_type: DeployType = DeployType.include_state_db,
    lakehouse_type: LakehouseOption = LakehouseOption.postgres,
) -> None:
    """
    Deploy the app to the Cloud Server.
    """

    if ctx.invoked_subcommand is not None:
        return

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()
    try:
        manager.cloud_actions_manager.create_deploy(
            deploy_type=deploy_type.value,
            lakehouse_type=lakehouse_type.value,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return
