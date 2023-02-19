import pathlib
from texteditor.extensions import generic

cfgs = {
    "section1": {
        "user": "lebao3105",
        "password": "hidden"
    },
    "section2": {
        "isrequired": "yes",
        "enabled": "no"
    }
}

config = generic.Setter(
    configs=cfgs,
    file="helloworld.ini",
    whatdir=str(pathlib.Path(__file__).parent)
)

print("Going to load: %s" % str(pathlib.Path(__file__).parent/"helloworld.ini"))

def test_getconfig():
    assert config.call("section2", "isrequired") == "yes", "Option not found or returns unexpected value"

def test_editconfig():
    config.set("section1", "user", "anonymous")
    assert config.call("section1", "user") == "anonymous", "Option not changed!"