import click
import ConfigParser
import os
import shutil
import random
import string
from git import Git

@click.group()
@click.option('--verbose', '-v', is_flag=True, default=False, help="Run dot in verbose mode.")
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
    check_init(ctx)

    if not os.path.exists(trackfile_path()):
        click.secho('Pssst...you aren\'t tracking any files.\nTry running `dot track [filename]`.', fg='yellow', bold=True)
        ctx.abort()

    with open(trackfile_path(), 'r') as trf:
        for line in trf:
            line = line.rstrip()
            VerboseLog('Copying ' + line + ' to ' + dot_dir_path() + '/' + line, ctx)
            shutil.copyfile(home() + '/' + line, dot_dir_path() + '/' + line)

    VerboseLog('Creating Git class object, running git.push()', ctx)
    git = Git(home(), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    return_code = git.push()

    VerboseLog('git.push() return codes were ' +
                str(return_code[0]) + ' ' + 
                str(return_code[1]) + ' ' + 
                str(return_code[2]), ctx)

    if return_code[1] != 0 and return_code[2] == 0:
        click.echo("No dotfile changes to push.")
    elif return_code[2] != 0:
        click.echo("There was a problem pushing the changes.")

@main.command(help="Pull dotfile changes using git.")
@click.pass_context
def pull(ctx):
    """Pull dotfile changes from GitHub"""

    VerboseLog('Running pull()', ctx)
    check_init(ctx)

    if not os.path.exists(trackfile_path()):
        click.secho('Pssst...you aren\'t tracking any files.\nTry running `dot track [filename]`.', fg='yellow', bold=True)
        ctx.abort()

    with open(trackfile_path(), 'r') as trf:
        for line in trf:
            line = line.rstrip()
            VerboseLog('Copying ' + dot_dir_path() + '/' + line + ' to ' + home() + '/' + line, ctx)
            shutil.copyfile(home() + '/' + line, dot_dir_path() + '/' + line)

    VerboseLog('Creating Git class object, running git.pull()', ctx)
    git = Git(home(), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
    return_code = git.pull()

    VerboseLog('git.pull() return code was ' + str(return_code), ctx)

@main.command(help="Add files to dot's tracking.")
@click.argument('filename')
@click.pass_context
def track(ctx, filename):
    """Add files to dot's tracking"""
    
    VerboseLog('Running track()', ctx)
    check_init(ctx)

    trackfile = trackfile_path()
    
    with open(trackfile, 'a+') as tf:
        tf.write(filename + "\n")

    click.echo('Now tracking ' + filename)

@main.command(help="Clean dot to start over.")
@click.pass_context
def clean(ctx):
    """Clean dot to start over"""

    VerboseLog('Running clean()', ctx)
    check_init(ctx)

    click.echo('Removing .dotconfig')
    if config_exists():
        os.remove(config_file_path())

    click.echo('Removing ~/.dot/')
    if os.path.isdir(dot_dir_path()):
        shutil.rmtree(dot_dir_path())

    if not config_exists() and not os.path.isdir(dot_dir_path()):
        click.secho('Clean completed.', fg='green')
    else:
        click.secho('Clean failed.', fg='red')

@main.command(help="Change configuration options.")
@click.argument('option')
@click.argument('value')
@click.pass_context
def config(ctx, option, value):
    """Change configuration options"""

    VerboseLog('Running config()', ctx)
    check_init(ctx)

    Config = ConfigParser.ConfigParser()
    Config.read(config_file_path())

    with open(config_file_path(), 'w+') as cf:
        Config.set('options', option, value)
        Config.write(cf)

    click.secho(option + " set to " + value, fg='green')
    

@main.command(help="Run initial setup.")
@click.pass_context
def init(ctx):
    """Run initial setup"""

    VerboseLog('Running init()', ctx)

    config_file = config_file_path()
    Config = ConfigParser.ConfigParser()

    if not config_exists():
        VerboseLog('Initializing first set up.', ctx)

        f = open(config_file, 'w+')
        os.makedirs(dot_dir_path())

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

        git = Git(home(), GetConfig("options")['gitname'], GetConfig("options")['reponame'])
        return_code = git.clone()
        VerboseLog("git.clone() return_code was " + str(return_code), ctx)
        if return_code == 0:
            click.secho('\ndot is initalized. Run `dot pull` to pull dotfiles,\nor `dot track [dotfile]` if you\'ve never\nused dot. Also see `dot --help`.\n', fg='green')
        else:
            click.secho('\ndot could not pull your repo from GitHub.\nRun `dot clean` followed by `dot init`\nto start over.\n\n(You may want to check your prerequisites\nat https://github.com/kylefrost/dot#prerequisites.)\n', fg='red')
    else:
        VerboseLog('Is not initial set up.', ctx)
        click.secho('You already set up dot. Run `dot config [option] [value]` to\nchange a config value, or edit ' + config_file + '. To start\nover, run `dot clean`.\n', fg='yellow')



"""                       """
""" Non-command functions """
"""                       """

def VerboseLog(message, ctx):
    """Log verbose messages"""
    if ctx.obj['verbose']:
        click.secho('VERBOSE: ' + message, fg='blue')

def GetConfig(section):
    """Read config file sections"""
    Config = ConfigParser.ConfigParser()
    Config.read(config_file_path())
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print "error"
        except:
            print "exception on %s!" % option
            dict1[option] = None
    return dict1

def config_exists():
    """Determine if config file exists and return boolean"""
    return os.path.isfile(config_file_path())

def config_file_path():
    """Return config file path as string"""
    return home() + "/.dotconfig"

def dot_dir_path():
    """Return dot directory path as string"""
    return home() + "/.dot"

def trackfile_path():
    """Return trackfile path as string"""
    return dot_dir_path() + "/.trackfile"

def check_init(ctx):
    if not config_exists():
        click.secho('\ndot not set up. Use `dot init` to begin.\n', fg='red')
        ctx.abort()

# TODO: Implement dynamic home, replace instances of os.path.expanduser("~") with home()
def home():
    """Determine home and return as string"""
    return os.path.expanduser("~")

# TODO: Implement choice of git hosting site, add to init of Git() class object
#       for use when interacting with git
def githost():
    """Read githost from config file and return as string"""
    pass
