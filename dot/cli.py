import click
import ConfigParser
import os
import shutil
from git import Git

Config = ConfigParser.ConfigParser()

@click.group()
@click.option('--verbose', is_flag=True, default=False, help="Run dot in verbose mode.")
@click.pass_context
def main(ctx, verbose):
    """Lightweight tool for managing dotfiles with git and the command line"""

    ctx.obj = {}
    ctx.obj['verbose'] = verbose

    VerboseLog('Running dot...', ctx)

@main.command(help="Push dotfile changes using git.")
@click.pass_context
def push(ctx):
    """Push dotfile changes to GitHub"""

    VerboseLog('Running push()', ctx)
    Config.read(os.path.expanduser("~") + "/.dotconfig")

    VerboseLog('Creating Git class object, running git.push()', ctx)
    git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    return_code = git.push()

    VerboseLog('git.push() return code was ' + return_code, ctx)

@main.command(help="Pull dotfile changes using git.")
@click.pass_context
def pull(ctx):
    """Pull dotfile changes from GitHub"""

    VerboseLog('Running pull()', ctx)
    Config.read(os.path.expanduser("~") + "/.dotconfig")

    VerboseLog('Creating Git class object, running git.pull()', ctx)
    git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    return_code = git.pull()

    VerboseLog('git.pull() return code was ' + return_code, ctx)

@main.command(help="Add files to dot's tracking.")
@click.pass_context
def track(ctx):
    """Add files to dot's tracking"""
    
    VerboseLog('Running track()', ctx)
    pass

@main.command(help="Clean dot to start over.")
@click.pass_context
def clean(ctx):
    """Clean dot to start over"""

    VerboseLog('Running clean()', ctx)

    click.echo('Removing .dotconfig')
    if os.path.isfile(os.path.expanduser("~") + "/.dotconfig"):
        os.remove(os.path.expanduser("~") + "/.dotconfig")

    click.echo('Removing ~/.dot/')
    if os.path.isdir(os.path.expanduser("~") + "/.dot"):
        shutil.rmtree(os.path.expanduser("~") + "/.dot")

    if not os.path.isfile(os.path.expanduser("~") + "/.dotconfig") and not os.path.isdir(os.path.expanduser("~") + "/.dot"):
        click.echo('Clean completed.')
    else:
        click.echo('Clean failed.')

@main.command(help="Change configuration options.")
@click.pass_context
def config(ctx):
    """Change configuration options"""

    VerboseLog('Running config()', ctx)
    pass

@main.command(help="Run initial setup.")
@click.pass_context
def init(ctx):
    """Run initial setup"""

    VerboseLog('Running init()', ctx)

    config_file = os.path.expanduser("~") + "/.dotconfig"

    if not os.path.isfile(config_file):

        VerboseLog('Initializing first set up.', ctx)

        f = open(config_file, 'w+')
        os.makedirs(os.path.expanduser("~") + "/.dot/")

        Config.add_section('options')

        VerboseLog('Requesting user options for initial settings.', ctx)

        value = click.prompt('GitHub user name', confirmation_prompt=True)
        Config.set('options', 'gitname', value)

        value = click.prompt('GitHub repo name', default='dotfiles')
        Config.set('options', 'reponame', value)

        Config.write(f)
        f.close()

        VerboseLog('Options set.', ctx)
        VerboseLog('Cloning repo into $HOME/.dot/', ctx)

        Config.read(config_file)
        git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
        return_code = git.clone()
        VerboseLog("git.clone() return_code was " + str(return_code), ctx)
        if return_code == 0:
            click.echo("\ndot is initalized. Run `dot pull` to pull dotfiles,\nor `dot track [dotfile]` if you\'ve never\nused dot. Also see `dot --help`.")
        else:
            click.echo("\ndot could not pull your repo from GitHub. Please\nrun `dot config [option] [value]` if you mistyped your information,\nor check your prerequisites at https://github.com/kylefrost/dot#prerequisites.")
    else:
        VerboseLog('Is not initial set up.', ctx)
        click.echo('You already set up dot. Run `dot config [option] [value]` to\nchange a config value, or edit ' + config_file + '. To start\nover, remove ' + config_file + ' and ' + os.path.expanduser("~") + '/.dot/.')


def VerboseLog(message, ctx):
    """Log verbose messages"""
    if ctx.obj['verbose']:
        click.echo('VERBOSE: ' + message)

def GetConfig(section):
    """Read config file sections"""
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

# TODO: Implement check for config file existence, error if needed and not available
def config_exists():
    """Determine if config file exists and return boolean"""
    pass

# TODO: Get config file string and return
def config_file():
    """Return config file path as string"""
    pass

# TODO: Get dot git directory ($HOME/.dot/) and return
def dot_dir():
    """Return dot directory path as string"""
    pass

# TODO: Implement dynamic home, replace instances of os.path.expanduser("~") with home()
def home():
    """Determine home and return as string"""
    pass

# TODO: Implement choice of git hosting site, add to init of Git() class object
#       for use when interacting with git
def githost():
    """Read githost from config file and return as string"""
    pass
