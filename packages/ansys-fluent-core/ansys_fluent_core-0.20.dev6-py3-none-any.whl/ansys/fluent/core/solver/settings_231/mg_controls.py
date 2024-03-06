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

from .mg_controls_child import mg_controls_child

class mg_controls(NamedObject[mg_controls_child], _NonCreatableNamedObjectMixin[mg_controls_child]):
    """
    'mg_controls' child.
    """

    fluent_name = "mg-controls"

    child_object_type: mg_controls_child = mg_controls_child
    """
    child_object_type of mg_controls.
    """
