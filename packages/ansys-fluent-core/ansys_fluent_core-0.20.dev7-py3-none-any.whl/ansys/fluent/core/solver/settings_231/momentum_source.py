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

class momentum_source(ListObject[child_object_type_child]):
    """
    'momentum_source' child.
    """

    fluent_name = "momentum-source"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of momentum_source.
    """
