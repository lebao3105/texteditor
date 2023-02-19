import os
import os.path
import pathlib
import sys

from ..backend import get_config, logger, is_development_build


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
        self._filepath: str
        print(whatdir, file)

        if file == False:
            self._filename = get_config.file
        else:
            self._filename = file
        
        if whatdir == False:
            self._filepath = get_config.dird + get_config.appver.base_version
        else:
            self._filepath = whatdir
        
        if self._filename == get_config.file:
            self.cfg = get_config.GetConfig(configs, self._filename)
        else:
            self.cfg = get_config.GetConfig(configs, str(pathlib.Path(self._filepath) / self._filename))

    # Properties
    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self.filename = value

    @filename.deleter
    def filename(self):
        del self.filename, self._filename

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self.filepath = value

    @filepath.deleter
    def filepath(self):
        del self.filepath, self._filepath

    @property
    def default_filepath(self):
        if sys.platform == "win32":
            return os.environ["USERPROFILE"] + "\\.config\\texteditor\\extensions"
        else:
            return os.environ["HOME"] + "/.config/texteditor/extensions"

    @default_filepath.setter
    def default_filepath(self, value):
        self.default_filepath = value

    @default_filepath.deleter
    def default_filepath(self):
        del self.filepath

    # GetConfig shortcuts
    def call(self, section, option):
        return self.cfg.getvalue(section, option)

    def set(self, section, option, value):
        return self.cfg.change_config(section, option, value)


log = logger.GenericLogs()
global_settings = Setter(
    configs=get_config.cfg
)
