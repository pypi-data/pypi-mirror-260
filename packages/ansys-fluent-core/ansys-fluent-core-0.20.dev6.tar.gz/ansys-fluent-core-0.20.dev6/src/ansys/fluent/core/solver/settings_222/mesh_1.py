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

from .display import display as display_cls
from .mesh_child_1 import mesh_child

class mesh(NamedObject[mesh_child], _CreatableNamedObjectMixin[mesh_child]):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: mesh_child = mesh_child
    """
    child_object_type of mesh.
    """
