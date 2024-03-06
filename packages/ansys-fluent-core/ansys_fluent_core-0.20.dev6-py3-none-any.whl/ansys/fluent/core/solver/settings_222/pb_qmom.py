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

class pb_qmom(NamedObject[child_object_type_child], _CreatableNamedObjectMixin[child_object_type_child]):
    """
    'pb_qmom' child.
    """

    fluent_name = "pb-qmom"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of pb_qmom.
    """
