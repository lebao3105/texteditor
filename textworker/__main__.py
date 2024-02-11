import argparse
import os
import sys

from textworker import generic

ignore_not_exists: bool
create_new: bool

parser = argparse.ArgumentParser(
    sys.argv[0],
    description = \
    """
    A simple, cross-platform text editor.
    (C) 2022-2024 Le Bao Nguyen and contributors.
    Read documents online: https://lebao3105.gitbook.io/texteditor_doc
    Where the source code goes: https://github.com/lebao3105/texteditor
    """,
)
parser.add_argument("paths", nargs="*")

# Flags
config_flags = parser.add_argument_group("Configurations")
config_flags.add_argument(
    "--custom-config-dir",
    type=str,
    help="Load custom configuration(s) from a directory",
)
config_flags.add_argument(
    "--custom-data-dir",
    type=str,
    help="Load custom application data (should not be a relative path)",
)

file_flags = parser.add_argument_group("File-related flags")
file_flags.add_argument(
    "--create-new",
    "-c",
    const=False,
    nargs="?",
    help="Send 'yes' to any 'File not found' message",
)
file_flags.add_argument(
    "--ignore-not-exists",
    "-ig",
    const=False,
    nargs="?",
    help="Ignore all 'File not found' messages",
)

def main():
    global ignore_not_exists, create_new
    options = parser.parse_args()

    if options.ignore_not_exists and options.create_new:  # Conflict args
        parser.error("2 conlict arguments: --ignore-not-exists/-ig and --create-new/-c")

    if options.ignore_not_exists:
        ignore_not_exists = bool(options.ignore_not_exists)

    if options.create_new:
        create_new = bool(options.create_new)

    if options.custom_config_dir:
        options.custom_config_dir = os.path.normpath(options.custom_config_dir)
        generic.CONFIGS_PATH = generic.CONFIGS_PATH.replace(
            os.path.expanduser("~/.config/textworker"),
            os.path.normpath(options.custom_config_dir),
        )

    if options.custom_data_dir:
        generic.DATA_PATH = os.path.normpath(options.custom_data_dir)

    files: list[str] = []
    dirs: list[str] = []

    if options.paths:
        generic.logger.debug("Got paths: %s", " ".join(options.paths))
        for path in options.paths:
            if not os.path.isfile(path): dirs += [path]
            else: files += [path]

    import textworker.main as main_entrypoint
    main_entrypoint.start_app(files, dirs)

if __name__ == "__main__": main()