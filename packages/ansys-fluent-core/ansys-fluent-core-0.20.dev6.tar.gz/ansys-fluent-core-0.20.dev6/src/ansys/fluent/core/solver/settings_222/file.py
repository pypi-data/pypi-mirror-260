#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .read import read as read_cls
from .replace_mesh import replace_mesh as replace_mesh_cls
from .write import write as write_cls
from .parametric_project import parametric_project as parametric_project_cls
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    command_names = \
        ['read', 'replace_mesh', 'write', 'parametric_project']

    _child_classes = dict(
        read=read_cls,
        replace_mesh=replace_mesh_cls,
        write=write_cls,
        parametric_project=parametric_project_cls,
    )

