import click
import ConfigParser
import os

@click.group(invoke_without_command=True)
@click.option('--verbose', is_flag=True, default=False)
@click.pass_context
def main(ctx, verbose):
    """Easily manage dotfiles through the command line."""
    ctx.obj = {}
    ctx.obj['verbose'] = verbose
    if ctx.invoked_subcommand is None:
        click.echo('Running main...')

@main.command(help="Push dotfiles to GitHub.")
@click.pass_context
def push(ctx):
    """Push dotfile changes to GitHub."""
    click.echo('Pushing...')

@main.command(help="Pull dotfiles from GitHub.")
@click.pass_context
def pull(ctx):
    """Pull dotfile changes from GitHub repo."""
    click.echo('Pulling...')

@main.command(help="Change configuration options.")
@click.pass_context
def config(ctx):
    """Configure options for dot."""
    config_file = os.path.expanduser("~") + "/.dotconfig"
    isInitSetup = False

    if not os.path.isfile(config_file):
        isInitSetup = True

    """No .dotconfig, so set up from scratch (assume first run)"""
    if isInitSetup:
        VerboseLog('Initializing first set up', ctx)

        # Set up ConfigParser
        Config = ConfigParser.ConfigParser()

        # Open config file
        f = open(config_file, 'w+')

        # Add options section to .dotconfig
        Config.add_section('options')

        # Request home folder if not ~/
        value = click.prompt('Home folder', default=os.path.expanduser("~"))
        if not os.path.isdir(value):
            value = click.prompt(value + ' is not a valid directory', default='~/')

        Config.set('options', 'home', value)

        # Request GitHub user name
        value = click.prompt('GitHub user name', confirmation_prompt=True)

        Config.set('options', 'gitname', value)

        # Request GitHub repo name
        value = click.prompt('GitHub repo name', default='dotfiles')

        Config.set('options', 'reponame', value)

        Config.write(f)
        f.close()

        click.echo('Options set.')

"""Log verbose messages"""
def VerboseLog(message, ctx):
    if ctx.obj['verbose']:
        click.echo('VERBOSE: ' + message)
