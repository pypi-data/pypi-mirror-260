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

from .axis_child import axis_child

class degassing(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'degassing' child.
    """

    fluent_name = "degassing"

    child_object_type: axis_child = axis_child
    """
    child_object_type of degassing.
    """
