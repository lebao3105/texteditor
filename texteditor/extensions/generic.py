import os
import os.path
import pathlib
import platform
import shutil
import sys

from ..backend import get_config, logger


class Setter(object):
    def __init__(
        self,
        configs: dict[str, str],
        file: str | bool = False,
        whatdir: str | bool = False,
    ):
        """
        Configurations manager for texteditor/textworker.
        It works different from the textworker's AppSettings on
        the INI file format, and more functions to use than.

        :param configs (dict) : Default configurations
        :param file (str|bool=False) : Configuration file path. By default just use the file name,
                and Setter will find it on ~/.config/texteditor/extensions/. Set to False to disable it. (whetever you still need to use it neither)
        :param whatdir (str|bool=False) : Set the config file's directory. Set to False to disable it.

        Note:
        * If you don't specify any file path here, the class will use texteditor's config file by default.
        """
        self._filename: str
        self._filepath: str = os.path.expanduser(
            "~/.config/texteditor/extensions"
        )  # Although this Tk version is going to be gone away...

        if file == False:
            self._filename = get_config.file
        else:
            self._filename = file

        if whatdir == False:
            self._filepath = get_config.dird
        else:
            self._filepath = whatdir

        if self._filename == get_config.file:
            self.cfg = get_config.GetConfig(configs, self._filename)
        else:
            self.cfg = get_config.GetConfig(
                configs, str(pathlib.Path(self._filepath) / self._filename)
            )

    # GetConfig shortcuts
    def call(self, section, option):
        return self.cfg.getvalue(section, option)

    def set(self, section, option, value):
        return self.cfg.change_config(section, option, value)


log = logger.GenericLogs()
global_settings = Setter(configs=get_config.cfg)
separator = "/" if platform.system() != "Windows" else "\\"


def CreateDirectory(path: str, subdirs: list[str] = []):
    """
    Create a directory with sub directories.
    """
    if not os.path.isdir(path):
        os.mkdir(path)
    if subdirs:
        for folder in subdirs:
            folder = CraftDir(path, folder)
            if not os.path.isdir(folder):
                os.mkdir(folder)


def CraftDir(path: str, subdir: str) -> str:
    return str(pathlib.Path(path) / subdir)


def CraftDirWithFile(path: str, filename: str) -> str:
    return str(pathlib.Path(path) / filename)


def WalkCreation(directory: str):
    """
    I don't know how to describe this function.
    :raises Exception: Directory creation failed
    """
    directory = os.path.normpath(directory)
    splits = directory.split(separator)
    firstdir = splits[0]
    for item in range(1, len(splits)):
        firstdir += separator + splits[item]
        if not os.path.isdir(firstdir):
            os.mkdir(firstdir)


def GetCurrentDir(file: str, aspathobj: bool = False):
    result = pathlib.Path(file).parent
    if aspathobj:
        return result
    return result.__str__()


def ResetEveryConfig():
    """
    Reset every configurations under ~/.config/textworker to default.
    Will close the app after completed.
    """
    shutil.rmtree(os.path.expanduser("~/.config/texteditor"), ignore_errors=True)
    CreateDirectory(os.path.expanduser("~/.config/texteditor"))
    sys.exit()
