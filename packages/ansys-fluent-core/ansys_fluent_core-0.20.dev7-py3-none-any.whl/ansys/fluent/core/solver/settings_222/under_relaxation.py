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

from .relaxation_factor_child import relaxation_factor_child

class under_relaxation(NamedObject[relaxation_factor_child], _CreatableNamedObjectMixin[relaxation_factor_child]):
    """
    Enter Under Relaxation Menu.
    """

    fluent_name = "under-relaxation"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of under_relaxation.
    """
