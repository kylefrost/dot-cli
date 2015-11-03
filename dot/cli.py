import click


@click.command()
@click.option('push', default=None, help="Push dotfiles to GitHub.")
@click.argument('name', default='world', required=False)
def push(name, as_cowboy):
    """Easily manage dotfiles through the command line."""
    greet = 'Howdy' if as_cowboy else 'Hello'
    click.echo('{0}, {1}.'.format(greet, name))
