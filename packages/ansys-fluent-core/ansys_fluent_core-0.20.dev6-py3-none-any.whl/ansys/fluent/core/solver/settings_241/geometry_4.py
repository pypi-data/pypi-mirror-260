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

from .parts import parts as parts_cls
from .list_topology import list_topology as list_topology_cls
class geometry(Group):
    """
    'geometry' child.
    """

    fluent_name = "geometry"

    child_names = \
        ['parts']

    command_names = \
        ['list_topology']

    _child_classes = dict(
        parts=parts_cls,
        list_topology=list_topology_cls,
    )

