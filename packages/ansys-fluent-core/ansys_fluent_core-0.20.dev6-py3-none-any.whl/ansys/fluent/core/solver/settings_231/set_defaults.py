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

from .set_defaults_child import set_defaults_child

class set_defaults(NamedObject[set_defaults_child], _NonCreatableNamedObjectMixin[set_defaults_child]):
    """
    'set_defaults' child.
    """

    fluent_name = "set-defaults"

    child_object_type: set_defaults_child = set_defaults_child
    """
    child_object_type of set_defaults.
    """
