import xml.etree.ElementTree as ET
import typing

from ..generic import DATA_PATH

class TEProj:
    """
    Workspace/projects support for textworker.
    """

    kind: typing.Literal["blank", "make", "cmake", "gui"]
    language: typing.Literal["cpp", "c", "py"]
    localize: bool
    folderPaths: list[str]

    vcinit: typing.Literal["svn", "git"]
    repo: str

    uselicense: str # Here we go again (libtextworker moment)

    def beforeDoingAnyThing(this):
        assert this.kind
        assert this.language
        assert this.folderPaths

    