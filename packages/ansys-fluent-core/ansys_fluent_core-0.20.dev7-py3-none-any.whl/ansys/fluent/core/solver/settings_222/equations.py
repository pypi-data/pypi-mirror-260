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

from .equations_child import equations_child

class equations(NamedObject[equations_child], _CreatableNamedObjectMixin[equations_child]):
    """
    'equations' child.
    """

    fluent_name = "equations"

    child_object_type: equations_child = equations_child
    """
    child_object_type of equations.
    """
