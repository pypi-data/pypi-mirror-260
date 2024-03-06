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

from .axis_direction_component_child import axis_direction_component_child

class band_diffuse_frac(NamedObject[axis_direction_component_child], _CreatableNamedObjectMixin[axis_direction_component_child]):
    """
    'band_diffuse_frac' child.
    """

    fluent_name = "band-diffuse-frac"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of band_diffuse_frac.
    """
