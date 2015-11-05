import click
import ConfigParser
import os
from git import Git

Config = ConfigParser.ConfigParser()

@click.group()
@click.option('--verbose', is_flag=True, default=False, help="Run dot in verbose mode.")
@click.pass_context
def main(ctx, verbose):
    """Easily manage dotfiles through the command line."""
    ctx.obj = {}
    ctx.obj['verbose'] = verbose
    VerboseLog('Running dot...', ctx)
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
    VerboseLog('Pulling dotfiles from repo...', ctx)
    Config.read(os.path.expanduser("~") + "/.dotconfig")
    git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    git.pull()

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
        VerboseLog('Initializing first set up.', ctx)

        # Open config file and create dir
        f = open(config_file, 'w+')
        os.makedirs(os.path.expanduser("~") + "/.dot/")

        # Add options section to .dotconfig
        Config.add_section('options')

        VerboseLog('Requesting user options for initial settings.', ctx)
        # Request home folder if not ~/
        #value = click.prompt('Home folder', default=os.path.expanduser("~"))
        #if not os.path.isdir(value):
            #value = click.prompt(value + ' is not a valid directory', default=os.path.expanduser("~"))

        #Config.set('options', 'home', value)
        #os.makedirs(value + "/.dot/")

        # Request GitHub user name
        value = click.prompt('GitHub user name', confirmation_prompt=True)

        Config.set('options', 'gitname', value)

        # Request GitHub repo name
        value = click.prompt('GitHub repo name', default='dotfiles')

        Config.set('options', 'reponame', value)

        Config.write(f)
        f.close()

        VerboseLog('Options set.', ctx)
        VerboseLog('Cloning repo into $HOME/.dot/', ctx)

        Config.read(os.path.expanduser("~") + "/.dotconfig")
        git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
        git.clone()
        click.echo('dot is initalized. Run `dot pull` to set files, or `dot push` if this is your first time using dot.')
    else:
        VerboseLog('Is not initial set up.', ctx)
        click.echo('You already set up dot. Run dot config [option] [value] to change config, or edit ' + os.path.expanduser("~") + '/.dotconfig')
        return False


"""Log verbose messages"""
def VerboseLog(message, ctx):
    if ctx.obj['verbose']:
        click.echo('VERBOSE: ' + message)

"""Read config file sections quickly"""
def GetConfig(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print "error"
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# TODO: Implement dynamic home, replace instances of os.path.expanduser("~") with home()
"""Pulls home from file and returns string"""
def home():
    pass
