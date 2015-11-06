import click
import ConfigParser
import os
from git import Git

Config = ConfigParser.ConfigParser()

@click.group()
@click.option('--verbose', is_flag=True, default=False, help="Run dot in verbose mode.")
@click.pass_context
def main(ctx, verbose):
    """Lightweight tool for managing dotfiles with git and the command line"""

    VerboseLog('Running dot...', ctx)
    ctx.obj = {}
    ctx.obj['verbose'] = verbose

@main.command(help="Push dotfile changes to GitHub.")
@click.pass_context
def push(ctx):
    """Push dotfile changes to GitHub"""

    VerboseLog('Running push()', ctx)
    Config.read(os.path.expanduser("~") + "/.dotconfig")

    VerboseLog('Creating Git class object, running git.push()', ctx)
    git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    return_code = git.push()

    VerboseLog('git.push() return code - ' + return_code, ctx)

@main.command(help="Pull dotfile changes from GitHub.")
@click.pass_context
def pull(ctx):
    """Pull dotfile changes from GitHub repo"""

    VerboseLog('Running pull()', ctx)
    Config.read(os.path.expanduser("~") + "/.dotconfig")

    VerboseLog('Creating Git class object, running git.pull()', ctx)
    git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    return_code = git.pull()

    VerboseLog('git.pull() return code - ' + return_code, ctx)

@main.command(help="Add files to dot's tracking.")
@click.pass_context
def track(ctx):
    """Add files to dot's tracking"""
    
    VerboseLog('Running track()', ctx)
    pass

@main.command(help="Change or add configuration options.")
@click.pass_context
def config(ctx):
    """Change or add configuration options"""
    config_file = os.path.expanduser("~") + "/.dotconfig"

    if not os.path.isfile(config_file):

        VerboseLog('Initializing first set up.', ctx)

        f = open(config_file, 'w+')
        os.makedirs(os.path.expanduser("~") + "/.dot/")

        Config.add_section('options')

        VerboseLog('Requesting user options for initial settings.', ctx)
        # Request home folder if not ~/
        #value = click.prompt('Home folder', default=os.path.expanduser("~"))
        #if not os.path.isdir(value):
            #value = click.prompt(value + ' is not a valid directory', default=os.path.expanduser("~"))

        #Config.set('options', 'home', value)
        #os.makedirs(value + "/.dot/")

        value = click.prompt('GitHub user name', confirmation_prompt=True)
        Config.set('options', 'gitname', value)

        value = click.prompt('GitHub repo name', default='dotfiles')
        Config.set('options', 'reponame', value)

        Config.write(f)
        f.close()

        VerboseLog('Options set.', ctx)
        VerboseLog('Cloning repo into $HOME/.dot/', ctx)

        Config.read(os.path.expanduser("~") + "/.dotconfig")
        git = Git(os.path.expanduser("~"), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
        return_code = git.clone()
        VerboseLog("git.clone() return_code - " + str(return_code), ctx)
        if return_code == 0:
            click.echo("\ndot is initalized. Run `dot pull` to pull dotfiles,\nor `dot push` or `dot track [dotfile]` if you\'ve never\nused dot. Also see `dot --help`.")
        else:
            click.echo("\ndot could not pull your repo from GitHub. Please\nrun `dot config` again if you mistyped your information,\nor check your prerequisites on https://github.com/kylefrost/dot.")
    else:
        VerboseLog('Is not initial set up.', ctx)
        click.echo('You already set up dot. Run dot config [option] [value] to change a config value, or edit ' + os.path.expanduser("~") + '/.dotconfig.')


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

# TODO: Implement dynamic home, replace instances of os.path.expanduser("~") with home()
def home():
    """Read home from config file and return as string"""
    pass

# TODO: Implement choice of git hosting site, add to init of Git() class object
#       for use when interacting with git
def githost():
    """Read githost from config file and return as string"""
    pass
