from setuptools import setup, find_packages
from pathlib import Path

currdir = Path(__file__).parent
long_des = (currdir / "README.md").read_text(encoding="utf8")

setup (
    name='texteditor',
    author='Le Bao Nguyen',
    version='1.3.beta',
    url='https://github.com/lebao3105/texteditor',
    description='A Tkinter text editor',
    license="GPL v3",
    long_description=long_des,
    long_description_content_type='text/markdown',
    install_requires=[
        'configparser'
    ],
    entry_points = {
        'gui_scripts': [
            'texteditor = texteditor:start'
        ]
    },
    include_package_data=True,
    packages=find_packages(),
    package_data={
        "texteditor": ["icons/*.png"]
    }
)