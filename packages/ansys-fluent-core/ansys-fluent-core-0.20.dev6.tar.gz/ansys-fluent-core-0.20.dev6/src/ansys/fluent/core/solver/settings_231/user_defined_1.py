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

from .user_defined_child import user_defined_child

class user_defined(NamedObject[user_defined_child], _CreatableNamedObjectMixin[user_defined_child]):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    child_object_type: user_defined_child = user_defined_child
    """
    child_object_type of user_defined.
    """
