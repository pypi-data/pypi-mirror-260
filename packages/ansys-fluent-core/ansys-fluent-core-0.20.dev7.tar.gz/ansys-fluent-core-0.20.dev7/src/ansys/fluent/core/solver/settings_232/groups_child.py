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

from .components_2 import components as components_cls
from .list_properties_4 import list_properties as list_properties_cls
class groups_child(Group):
    """
    'child_object_type' of groups.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['components']

    command_names = \
        ['list_properties']

    _child_classes = dict(
        components=components_cls,
        list_properties=list_properties_cls,
    )

