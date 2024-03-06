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
from .pressure_inlet_child import pressure_inlet_child

class pressure_inlet(NamedObject[pressure_inlet_child], _CreatableNamedObjectMixin[pressure_inlet_child]):
    """
    'pressure_inlet' child.
    """

    fluent_name = "pressure-inlet"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: pressure_inlet_child = pressure_inlet_child
    """
    child_object_type of pressure_inlet.
    """
