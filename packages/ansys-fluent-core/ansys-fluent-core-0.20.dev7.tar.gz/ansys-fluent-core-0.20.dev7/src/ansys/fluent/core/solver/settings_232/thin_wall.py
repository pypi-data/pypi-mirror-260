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

from .list_properties_1 import list_properties as list_properties_cls
from .shell_conduction_child import shell_conduction_child

class thin_wall(ListObject[shell_conduction_child]):
    """
    'thin_wall' child.
    """

    fluent_name = "thin-wall"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: shell_conduction_child = shell_conduction_child
    """
    child_object_type of thin_wall.
    """
