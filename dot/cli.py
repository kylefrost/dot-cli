import click

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Easily manage dotfiles through the command line."""
    if ctx.invoked_subcommand is None:
        click.echo('Running main...')

@main.command(help="Test")
@click.pass_obj
def push(ctx):
    click.echo('Pushing...')
