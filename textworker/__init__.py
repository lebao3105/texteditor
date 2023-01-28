import gettext
import locale
import pathlib

from . import main
from . import backend, extensions
from .backend import is_development_build, get_config, __version__ as version, logger

currdir = pathlib.Path(__file__).parent

# Setup translation first
try:
    from textworker.defs import LOCALE_DIR, ICON_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"
    ICON_DIR = currdir / "icons"


locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")

_ = gettext.gettext
backend._ = _
extensions._ = _

# Icon
if is_development_build() == True:
    icon = str(ICON_DIR / "textworker.Devel.png")
else:
    icon = str(ICON_DIR / "textworker.png")

# Version
__version__ = version

cfg = get_config.GetConfig(get_config.cfg, get_config.file, default_section="interface")
log = logger.Logger()

del LOCALE_DIR, ICON_DIR

if __name__ == '__main__':
    main.start_app()
