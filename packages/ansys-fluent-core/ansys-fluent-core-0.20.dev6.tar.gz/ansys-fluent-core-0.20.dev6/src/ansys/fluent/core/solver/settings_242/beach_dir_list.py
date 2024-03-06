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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .beach_dir_list_child import beach_dir_list_child

class beach_dir_list(ListObject[beach_dir_list_child]):
    """
    Multi-Directional Beach Inputs.
    """

    fluent_name = "beach-dir-list"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: beach_dir_list_child = beach_dir_list_child
    """
    child_object_type of beach_dir_list.
    """
