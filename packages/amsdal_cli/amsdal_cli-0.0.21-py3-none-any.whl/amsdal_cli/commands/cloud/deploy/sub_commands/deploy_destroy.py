from pathlib import Path

from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app


@deploy_sub_app.command(name='destroy')
def destroy_command(deployment_id: str) -> None:
    """
    Destroy the app on the Cloud Server.
    """
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.destroy_deploy(deployment_id)
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    print(
        '[green]Destroying process is in progress now. '
        'After a few minutes, you can check the status of your deployment.[/green]'
    )
