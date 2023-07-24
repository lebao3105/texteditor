import argparse
import os
import pathlib
import sys

import libtextworker
from libtextworker.general import CraftItems
from texteditor import __version__
from texteditor import main as main_entrypoint

parser = argparse.ArgumentParser(
    sys.argv[0],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=f"""
    Texteditor version {__version__}
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
    nargs=1,
    type=str,
    help="Load custom configuration(s) from a directory",
)
config_flags.add_argument(
    "--custom-data-dir",
    type=str,
    nargs=1,
    const=str(pathlib.Path(__file__).parent / "data"),
    help="Custom application data directory (defaults to <script dir>/data)"
)
config_flags.add_argument(
    "--custom-libtew-dir",
    type=str,
    nargs=1,
    const=str(pathlib.Path(__file__).parent / ".." / "libtextworker"),
    help="Custom libtextworker path (useful for debugging)"
)

file_flags = parser.add_argument_group("File-related flags")
file_flags.add_argument(
    "--create-new",
    "-c",
    const="False",
    nargs=1,
    type=bool,
    help="Send 'yes' to any 'File not found' message",
)
file_flags.add_argument(
    "--ignore-not-exists",
    "-ig",
    const="False",
    nargs=1,
    type=bool,
    help="Ignore all 'File not found' messages",
)
# file_flags.add_argument("--open-directory", "-d", help="Open a directory")


def main():
    options = parser.parse_args()

    if options.ignore_not_exists and options.create_new:  # Conflict args
        parser.error("2 conlict arguments: --ignore-not-exists/-ig and --create-new/-c")

    if options.ignore_not_exists:
        main_entrypoint.ignore_not_exists = options.ignore_not_existt

    if options.create_new:
        main_entrypoint.create_new = options.create_new

    if options.custom_config_dir:
        options.custom_config_dir = os.path.abspath(options.custom_config_dir)
        libtextworker.THEMES_DIR = CraftItems(options.custom_config_dir, "/themes/")
        libtextworker.EDITOR_DIR = CraftItems(
            options.custom_config_dir, "/editorconfigs/"
        )
    
    if options.custom_data_dir:
        options.custom_data_dir = os.path.abspath(options.custom_data_dir)
        if not os.path.exists(options.custom_data_dir): raise NotADirectoryError(f"Custom data dir not found: {options.custom_data_dir}")
        sys.path.append(options.custom_data_dir)
    
    if options.custom_libtew_dir:
        options.custom_data_dir = os.path.abspath(options.custom_libtew_dir)
        if not os.path.exists(options.custom_data_dir): raise NotADirectoryError(f"Custom libtextworker dir not found: {options.custom_libtew_dir}")
        sys.path.append(options.custom_libtew_dir)

    if options.files:
        files = options.files
    else:
        files = []

    # if options.open_directory:
    #     dir = options.open_directory
    # else:
    #     dir = None

    main_entrypoint.start_app(files)


if __name__ == "__main__":
    main()
