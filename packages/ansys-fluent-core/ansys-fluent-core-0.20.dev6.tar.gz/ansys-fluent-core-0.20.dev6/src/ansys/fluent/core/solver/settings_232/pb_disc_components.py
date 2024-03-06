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
from .child_object_type_child_1 import child_object_type_child

class pb_disc_components(ListObject[child_object_type_child]):
    """
    'pb_disc_components' child.
    """

    fluent_name = "pb-disc-components"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of pb_disc_components.
    """
