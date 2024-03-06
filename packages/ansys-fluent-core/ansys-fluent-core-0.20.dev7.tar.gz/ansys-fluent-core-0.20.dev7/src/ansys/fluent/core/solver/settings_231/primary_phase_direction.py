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

from .child_object_type_child_1 import child_object_type_child

class primary_phase_direction(ListObject[child_object_type_child]):
    """
    'primary_phase_direction' child.
    """

    fluent_name = "primary-phase-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of primary_phase_direction.
    """
