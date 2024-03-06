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

from .axis_origin import axis_origin as axis_origin_cls
from .axis_direction import axis_direction as axis_direction_cls
from .radial_diffusivity import radial_diffusivity as radial_diffusivity_cls
from .tangential_diffusivity import tangential_diffusivity as tangential_diffusivity_cls
from .axial_diffusivity import axial_diffusivity as axial_diffusivity_cls
class cyl_orthotropic(Group):
    """
    'cyl_orthotropic' child.
    """

    fluent_name = "cyl-orthotropic"

    child_names = \
        ['axis_origin', 'axis_direction', 'radial_diffusivity',
         'tangential_diffusivity', 'axial_diffusivity']

    _child_classes = dict(
        axis_origin=axis_origin_cls,
        axis_direction=axis_direction_cls,
        radial_diffusivity=radial_diffusivity_cls,
        tangential_diffusivity=tangential_diffusivity_cls,
        axial_diffusivity=axial_diffusivity_cls,
    )

