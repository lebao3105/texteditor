from setuptools import setup, find_packages
from pathlib import Path

currdir = Path(__file__).parent
long_des = (currdir / "README.md").read_text()

setup (
    name='texteditor',
    author='Le Bao Nguyen',
    version='1.3-dev',
    description='A Tkinter text editor',
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
    packages=find_packages()
)