from setuptools import setup, find_packages

setup (
    name='texteditor',
    author='Le Bao Nguyen',
    version='1.2',
    install_requires=[
        'configparser'
    ],
    package_data={'': ['texteditor/icons/texteditor.Devel.png']},
    include_package_data=True,
    packages=find_packages()
)