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

from .icing_child import icing_child

class icing(NamedObject[icing_child], _CreatableNamedObjectMixin[icing_child]):
    """
    'icing' child.
    """

    fluent_name = "icing"

    child_object_type: icing_child = icing_child
    """
    child_object_type of icing.
    """
