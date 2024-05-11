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


class SideBarPowerShellCommand(SideBarShellCommand):

    def run(self, paths):
        folder = self.get_folder(paths)
        os.environ['NO_THEME'] = '1'
        # 尝试检查是否存在 pwsh
        if self.check_command_exists("pwsh"):
            run_shell('start pwsh', cwd=folder)
        else:
            run_shell('start powershell', cwd=folder)

    def check_command_exists(self, command):
        """检查系统是否有指定的命令"""
        try:
            # 设置启动信息以隐藏窗口
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            # 执行命令并获取版本信息，不显示窗口
            proc = subprocess.Popen([command, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, startupinfo=startupinfo)
            proc.communicate()  # 等待命令执行完成
            return proc.returncode == 0
        except FileNotFoundError:
            return False

    def description(self):
        return 'Open in PowerShell'


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
