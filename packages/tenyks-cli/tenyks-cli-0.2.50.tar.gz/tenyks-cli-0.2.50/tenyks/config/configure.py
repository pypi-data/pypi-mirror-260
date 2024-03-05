import click

from tenyks.config.config import Config

current_config = Config.load()


@click.command()
@click.option(
    "--api_url",
    prompt="Enter API URL",
    help="The tenyks api url",
    default=current_config.api_url,
)
@click.option(
    "--username",
    prompt="Enter tenyks username",
    help="The tenyks username",
    default=current_config.username,
    required=False,
)
@click.option(
    "--password",
    prompt="Enter tenyks password",
    help="The tenyks password",
    hide_input=True,
    default=current_config.get_masked_password(),
    required=False,
)
@click.option(
    "--api_key",
    prompt="Enter tenyks API key",
    help="The tenyks API key",
    default=current_config.api_key,
    required=False,
)
@click.option(
    "--api_secret",
    prompt="Enter tenyks API secret",
    help="The tenyks API secret",
    hide_input=True,
    default=current_config.get_masked_api_secret(),
    required=False,
)
@click.option(
    "--workspace_name",
    prompt="Enter tenyks workspace name",
    help="The tenyks workspace name",
    prompt_required=False,
    default=current_config.workspace_name,
)
@click.option(
    "--default_task_type",
    prompt="Enter tenyks default task type",
    help="Enter tenyks default task type",
    prompt_required=False,
    default=current_config.default_task_type,
    type=click.Choice(current_config.get_default_task_types(), case_sensitive=True),
)
def configure(
    api_url: str,
    username: str,
    password: str,
    api_key: str,
    api_secret: str,
    workspace_name: str,
    default_task_type: str,
):
    if password == current_config.get_masked_password():
        # don't override the password with masked one
        password = current_config.password

    if api_secret == current_config.get_masked_api_secret:
        # don't override the api_secret with masked one
        api_secret = current_config.api_secret

    if not (username and password) and not (api_key and api_secret):
        raise click.BadParameter(
            "You must provide either a username and password or an API key and secret."
        )

    Config(
        api_url=api_url,
        username=username,
        password=password,
        api_key=api_key,
        api_secret=api_secret,
        workspace_name=workspace_name,
        default_task_type=default_task_type,
    ).save()
