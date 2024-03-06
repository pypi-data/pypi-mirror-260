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

class shadow(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'shadow' child.
    """

    fluent_name = "shadow"

    child_object_type: axis_child = axis_child
    """
    child_object_type of shadow.
    """
