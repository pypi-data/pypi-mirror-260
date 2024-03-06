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

from .relative_permeability_1 import relative_permeability as relative_permeability_cls
from .capillary_pressure_as_diffusion import capillary_pressure_as_diffusion as capillary_pressure_as_diffusion_cls
class porous_media(Group):
    """
    Multiphase miscellaneous porous media numerics menu.
    """

    fluent_name = "porous-media"

    child_names = \
        ['relative_permeability', 'capillary_pressure_as_diffusion']

    _child_classes = dict(
        relative_permeability=relative_permeability_cls,
        capillary_pressure_as_diffusion=capillary_pressure_as_diffusion_cls,
    )

