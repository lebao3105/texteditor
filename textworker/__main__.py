import argparse
import sys
import textworker.main as main_entrypoint

import libtextworker
from libtextworker.general import CraftItems

parser = argparse.ArgumentParser(
    sys.argv[0],
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""A simple, cross-platform text editor.\n
        Read documents online: https://lebao3105.gitbook.io/texteditor_doc\n
        Where the source code goes: https://gitlab.com/lebao3105/texteditor
        """,
)
parser.add_argument("files", nargs="*", help="File(s) to open")

# Flags
config_flags = parser.add_argument_group("Configurations")
config_flags.add_argument(
    "--load-custom-config", "-l", type=str, help="Load custom configuration directory"
)

file_flags = parser.add_argument_group("File-related flags")
file_flags.add_argument(
    "--create-new",
    "-c",
    const="False",
    nargs="?",
    choices=["True", "False"],
    help="Send 'yes' to any 'File not found' message",
)
file_flags.add_argument(
    "--ignore-not-exists",
    "-ig",
    const="False",
    nargs="?",
    choices=["True", "False"],
    help="Ignore all 'File not found' messages",
)


if __name__ == "__main__":
    options = parser.parse_args()

    if options.ignore_not_exists and options.create_new:  # Conflict args
        parser.error("2 conlict arguments: --ignore-not-exists/-ig and --create-new/-c")

    if options.ignore_not_exists:
        main_entrypoint.ignore_not_exists = bool(options.ignore_not_exists)
    if options.create_new:
        main_entrypoint.create_new = bool(options.create_new)

    if options.load_custom_config:
        libtextworker.THEMES_DIR = CraftItems(options.load_custom_config, "/themes/")
        libtextworker.EDITOR_DIR = CraftItems(
            options.load_custom_config, "/editorconfigs/"
        )

    if options.files:
        files = options.files
    else:
        files = []

    main_entrypoint.start_app(files)
