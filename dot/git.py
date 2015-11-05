import os
import subprocess

class Git:
    """ Git Functionality for Python """
    
    _dotdir = "/.dot/"
    _github = "https://github.com/"

    def __init__(self, home, gitname, reponame):
        self.home = home
        self.gitname = gitname
        self.reponame = reponame
    
    def clone(self):
        dest_path = self.home + self._dotdir
        git_url = self._github + self.gitname + "/" + self.reponame + ".git"
        os.chdir(dest_path)
        with open(os.devnull, 'w') as fnull:
            return subprocess.call(["git", "clone", git_url, "."], stdout=fnull, stderr=subprocess.STDOUT)

    def pull(self):
        dest_path = self.home + _dotdir
        os.chdir(dest_path)
        with open(os.devnull, 'w+') as fnull:
            return subprocess.call(["git", "pull"], stdout=fnull, stderr=fnull)
