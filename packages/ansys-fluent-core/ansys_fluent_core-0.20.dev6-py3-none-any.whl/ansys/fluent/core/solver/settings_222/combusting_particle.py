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

class combusting_particle(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'combusting_particle' child.
    """

    fluent_name = "combusting-particle"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of combusting_particle.
    """
