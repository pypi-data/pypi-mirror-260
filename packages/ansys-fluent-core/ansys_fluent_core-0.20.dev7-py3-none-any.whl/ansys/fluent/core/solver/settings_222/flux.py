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

from .flux_child import flux_child

class flux(NamedObject[flux_child], _CreatableNamedObjectMixin[flux_child]):
    """
    'flux' child.
    """

    fluent_name = "flux"

    child_object_type: flux_child = flux_child
    """
    child_object_type of flux.
    """
