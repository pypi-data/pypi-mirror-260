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

from .diffusion_collision_integral import diffusion_collision_integral as diffusion_collision_integral_cls
from .viscosity_collision_integral import viscosity_collision_integral as viscosity_collision_integral_cls
class neutral_involved_interaction(Group):
    """
    'neutral_involved_interaction' child.
    """

    fluent_name = "neutral-involved-interaction"

    child_names = \
        ['diffusion_collision_integral', 'viscosity_collision_integral']

    _child_classes = dict(
        diffusion_collision_integral=diffusion_collision_integral_cls,
        viscosity_collision_integral=viscosity_collision_integral_cls,
    )

