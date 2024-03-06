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
from .list_all import list_all as list_all_cls
from .expert_child import expert_child

class expert(ListObject[expert_child]):
    """
    Expert options in Park's model.
    """

    fluent_name = "expert"

    command_names = \
        ['list_properties', 'resize', 'list_all']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
        list_all=list_all_cls,
    )

    child_object_type: expert_child = expert_child
    """
    child_object_type of expert.
    """
