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

from .injections_child import injections_child

class injections(NamedObject[injections_child], _CreatableNamedObjectMixin[injections_child]):
    """
    'injections' child.
    """

    fluent_name = "injections"

    child_object_type: injections_child = injections_child
    """
    child_object_type of injections.
    """
