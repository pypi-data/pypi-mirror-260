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

from .fluid_child import fluid_child

class mixture_species(NamedObject[fluid_child], _NonCreatableNamedObjectMixin[fluid_child]):
    """
    'mixture_species' child.
    """

    fluent_name = "mixture-species"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of mixture_species.
    """
