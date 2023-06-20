## texteditor on branch 'data'
This git branch contains shared application data(s) for both ```main``` and ```wip/wx``` branches:
* Configuration template
* Icons
* GitHub workflows

## Notes for maintainers
If the .Source svg updated but others (svg) are not, update it by [```App icon preview```](https://flathub.org/apps/org.gnome.design.AppIconPreview). (ya that's for Linux btw)

Make trans by running builder.py for (lib)textworker - requires gettext. If needed, please make a pull request.

Run github workflows from this branch.

You can make .deb, .rpm, and many more using fpm. See all available package formats: https://fpm.readthedocs.io/en/latest/packaging-types.html. Use makerelease.fpm to build, but this assumes that you're in textworker/data (submodule).
