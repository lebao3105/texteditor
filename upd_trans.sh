#!/bin/bash
# Shell script to update and generate new .pot file...

if [[ $1 == "--updated-strings" || $1 == "-upd" ]]; then
    echo "Generating new .mo files..."
    for i in $(ls -d po/*/); do
        msgfmt ${i%%/}/LC_MESSAGES/base -o ${i%%/}/LC_MESSAGES/base.mo
    done
    echo "Done!"
    exit 0

elif [[ $1 == "--new-template" || $1 == "-tep" ]]; then
    echo "Generating new .pot file..."
    xgettext -d base -o po/base.pot src/{main,tabs}.py src/pages/*.py
    for i in $(ls -d po/*/); do
        msgmerge -U ${i%%/}/LC*/base.po po/base.pot
    done
    echo "Done!"

elif [[ $1 == "--help" || $1 == "-h" ]]; then
    echo "$0 [options]"
    echo "--updated-strings | -upd : Re-generate .mo files"
    echo "--help | -h : Show this help"
    echo "--new-template | -tep : Re-generate .pot (translation template file)"
    exit 1

else
    echo "Invalid option!"
    echo "Use --help | -h to show available options you can use."
    exit 1
fi
