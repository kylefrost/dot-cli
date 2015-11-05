import os
import subprocess

class Git:
    """ Git Functionality for Dot """
    
    _dotdir = "/.dot/"
    _github = "git@github.com:"

    def __init__(self, home, gitname, reponame):
        self.home = home
        self.gitname = gitname
        self.reponame = reponame
    
    def clone(self):
        dest_path = self.home + self._dotdir
        git_url = self._github + self.gitname + "/" + self.reponame + ".git"
        os.chdir(dest_path)
        with open(os.devnull, 'w') as fnull:
            r = subprocess.call(["git", "clone", git_url, "."], stdout=fnull, stderr=subprocess.STDOUT)

            with open("README.md", 'a+') as readme:
                readme.write("\n\n### Managed by [dot](https://github.com/kylefrost/dot)")

        return r

    def pull(self):
        dest_path = self.home + self._dotdir
        os.chdir(dest_path)
        with open(os.devnull, 'w+') as fnull:
            r = subprocess.call(["git", "pull"], stdout=fnull, stderr=fnull)

        return r

    def push(self):
        path = self.home + self._dotdir
        os.chdir(path)
        with open(os.devnull, 'w+') as fnull:
            r = subprocess.call(["git", "push", "origin", "master"])

        return r
