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

from .change_type import change_type as change_type_cls
from .pressure_outlet_child import pressure_outlet_child

class pressure_outlet(NamedObject[pressure_outlet_child], _CreatableNamedObjectMixin[pressure_outlet_child]):
    """
    'pressure_outlet' child.
    """

    fluent_name = "pressure-outlet"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: pressure_outlet_child = pressure_outlet_child
    """
    child_object_type of pressure_outlet.
    """
