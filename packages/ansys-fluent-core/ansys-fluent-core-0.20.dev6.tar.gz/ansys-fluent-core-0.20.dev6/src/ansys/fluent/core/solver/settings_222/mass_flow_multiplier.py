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

from .child_object_type_child import child_object_type_child

class mass_flow_multiplier(NamedObject[child_object_type_child], _CreatableNamedObjectMixin[child_object_type_child]):
    """
    'mass_flow_multiplier' child.
    """

    fluent_name = "mass-flow-multiplier"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of mass_flow_multiplier.
    """
