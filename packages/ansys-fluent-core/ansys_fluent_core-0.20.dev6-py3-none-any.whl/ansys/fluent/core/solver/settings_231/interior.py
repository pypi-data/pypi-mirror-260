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

from .interior_child import interior_child

class interior(NamedObject[interior_child], _NonCreatableNamedObjectMixin[interior_child]):
    """
    'interior' child.
    """

    fluent_name = "interior"

    child_object_type: interior_child = interior_child
    """
    child_object_type of interior.
    """
