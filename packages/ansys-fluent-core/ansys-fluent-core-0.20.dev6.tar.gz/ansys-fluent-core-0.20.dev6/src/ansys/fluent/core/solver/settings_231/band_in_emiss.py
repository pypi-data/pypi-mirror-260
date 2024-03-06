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

class band_in_emiss(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'band_in_emiss' child.
    """

    fluent_name = "band-in-emiss"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of band_in_emiss.
    """
