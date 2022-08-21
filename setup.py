from setuptools import setup, find_packages

setup (
    name='texteditor',
    author='Le Bao Nguyen',
    version='1.2-dev',
    install_requires=[
        'configparser'
    ],
    packages=find_packages()
)