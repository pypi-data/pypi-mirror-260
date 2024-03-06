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

from .volumes import volumes as volumes_cls
from .interfaces import interfaces as interfaces_cls
from .list_physics import list_physics as list_physics_cls
class physics(Group, _ChildNamedObjectAccessorMixin):
    """
    'physics' child.
    """

    fluent_name = "physics"

    child_names = \
        ['volumes', 'interfaces']

    command_names = \
        ['list_physics']

    _child_classes = dict(
        volumes=volumes_cls,
        interfaces=interfaces_cls,
        list_physics=list_physics_cls,
    )

