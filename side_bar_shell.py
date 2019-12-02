import os
from subprocess import Popen
from .SideBar import *


def run_shell(*args, cwd=None, timeout=None):
    Popen(*args, shell=True, cwd=cwd)


class SideBarShellCommand(SideBarCommand):

    def get_folder(self, paths):
        path = self.get_path(paths)

        if not os.path.exists(path):
            self.window.status_message('No such path[{}] exists'.format(path))
            return None

        if os.path.isfile(path):
            folder, leaf = os.path.split(path)
        else:
            folder = path

        return folder

    def run(self, paths):
        folder = self.get_folder(paths)
        run_shell('start', cwd=folder)

    def description(self):
        return 'Open in Shell'


class SideBarGitShellCommand(SideBarShellCommand):

    def run(self, paths):
        folder = self.get_folder(paths)
        run_shell('git-bash', cwd=folder)

    def description(self):
        return 'Open in Git Shell'


class SideBarOpenFolderCommand(SideBarCommand):

    def is_visible(self, paths):
        return len(paths) == 1 and os.path.isdir(paths[0])

    def run(self, paths):
        folder = self.get_path(paths)
        self.window.run_command("open_dir", {"dir": folder})

    def description(self):
        return 'Open Folder'


if __name__ == '__main__':
    run_shell('start')
