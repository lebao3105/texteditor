## texteditor on branch 'data'
This git branch contains shared application data(s) for both ```main``` and ```wip/wx``` branches:
* Configuration template
* Icons
* GitHub workflows

## Notes for maintainers
If the .Source svg updated but others (svg) are not, update it by [```App icon preview```](https://flathub.org/apps/org.gnome.design.AppIconPreview). (ya that's for Linux)

Make trans by running builder.py for (lib)textworker - requires gettext. If needed, please make a pull request.

Run github workflows from this branch.

version.json is used for listing releases for textworker to fetch.

The version must match the one in GitHub.

"changelog" key is either "github" (give user the link to GitHub Releases) or "none" (download and show the CHANGELOG file)