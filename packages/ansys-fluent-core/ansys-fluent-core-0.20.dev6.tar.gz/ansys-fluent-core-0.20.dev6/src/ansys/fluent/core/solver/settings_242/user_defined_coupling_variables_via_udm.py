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
from .user_defined_coupling_variables_via_udm_child import user_defined_coupling_variables_via_udm_child

class user_defined_coupling_variables_via_udm(ListObject[user_defined_coupling_variables_via_udm_child]):
    """
    'user_defined_coupling_variables_via_udm' child.
    """

    fluent_name = "user-defined-coupling-variables-via-udm"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: user_defined_coupling_variables_via_udm_child = user_defined_coupling_variables_via_udm_child
    """
    child_object_type of user_defined_coupling_variables_via_udm.
    """
