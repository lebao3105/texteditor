import argparse
import sys

import libtextworker
import textworker.main as main_entrypoint
from libtextworker.general import CraftItems
from textworker import __version__

parser = argparse.ArgumentParser(
    sys.argv[0],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=f"""
    Textworker version {__version__}
    A simple, cross-platform text editor.
    Read documents online: https://lebao3105.gitbook.io/texteditor_doc
    Where the source code goes: https://gitlab.com/lebao3105/texteditor
    """,
)
parser.add_argument("files", nargs="*", help="File(s) to open")

# Flags
config_flags = parser.add_argument_group("Configurations")
config_flags.add_argument(
    "--custom-config-dir",
    "-l",
    type=str,
    help="Load custom configuration(s) from a directory",
)

file_flags = parser.add_argument_group("File-related flags")
file_flags.add_argument(
    "--create-new",
    "-c",
    const="False",
    nargs="?",
    help="Send 'yes' to any 'File not found' message",
)
file_flags.add_argument(
    "--ignore-not-exists",
    "-ig",
    const="False",
    nargs="?",
    help="Ignore all 'File not found' messages",
)
file_flags.add_argument("--open-directory", "-d", help="Open a directory")

if __name__ == "__main__":
    options = parser.parse_args()

    if options.ignore_not_exists and options.create_new:  # Conflict args
        parser.error("2 conlict arguments: --ignore-not-exists/-ig and --create-new/-c")

    if options.ignore_not_exists:
        main_entrypoint.ignore_not_exists = bool(options.ignore_not_exists)
    if options.create_new:
        main_entrypoint.create_new = bool(options.create_new)

    if options.custom_config_dir:
        libtextworker.THEMES_DIR = CraftItems(options.custom_config_dir, "/themes/")
        libtextworker.EDITOR_DIR = CraftItems(
            options.custom_config_dir, "/editorconfigs/"
        )

    if options.files:
        files = options.files
    else:
        files = []

    if options.open_directory:
        dir = options.open_directory
    else:
        dir = None

    main_entrypoint.start_app(files, dir)
