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

from .injection_child import injection_child

class injection(NamedObject[injection_child], _CreatableNamedObjectMixin[injection_child]):
    """
    'injection' child.
    """

    fluent_name = "injection"

    child_object_type: injection_child = injection_child
    """
    child_object_type of injection.
    """
