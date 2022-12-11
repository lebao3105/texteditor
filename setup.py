from pathlib import Path
from setuptools import find_packages, setup
from texteditor.backend import constants

currdir = Path(__file__).parent
long_des = (currdir / "README.md").read_text(encoding="utf8")

if constants.STATE == "DEV":
    print("You are in a development build of texteditor")
else:
    print("You are in a stable build of texteditor - maybe?")

setup(
    name="texteditor",
    author="Le Bao Nguyen",
    version="1.4a2",
    url="https://github.com/lebao3105/texteditor",
    description="A Tkinter text editor",
    long_description=long_des,
    long_description_content_type="text/markdown",
    install_requires=["configparser", "darkdetect", "sv_ttk", "pygubu"],
    entry_points={"gui_scripts": ["texteditor = texteditor:start_app"]},
    include_package_data=True,
    packages=find_packages(),
    package_data={
        "texteditor": ["icons/*.png", "../po/*/LC_MESSAGES/*.mo", "views/*.ui"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Text Editors",
    ],
)
