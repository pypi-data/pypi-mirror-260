import click

from praetorian_cli.sdk.account import Account
from praetorian_cli.handlers.backend import chaos


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
@click.option('--backend', default='United States', help='The keychain backend to use', show_default=True)
def cli(ctx, backend):
    ctx.obj = Account(backend=backend)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


cli.add_command(chaos)


if __name__ == '__main__':
    cli()
