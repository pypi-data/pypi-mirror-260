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

from .diffusion_rate_constant import diffusion_rate_constant as diffusion_rate_constant_cls
from .pre_exponential_factor import pre_exponential_factor as pre_exponential_factor_cls
from .activation_energy import activation_energy as activation_energy_cls
from .char_porosity import char_porosity as char_porosity_cls
from .mean_pore_radius import mean_pore_radius as mean_pore_radius_cls
from .specific_internal_surface_area import specific_internal_surface_area as specific_internal_surface_area_cls
from .tortuosity import tortuosity as tortuosity_cls
from .burning_mode import burning_mode as burning_mode_cls
class intrinsic_model(Group):
    """
    'intrinsic_model' child.
    """

    fluent_name = "intrinsic-model"

    child_names = \
        ['diffusion_rate_constant', 'pre_exponential_factor',
         'activation_energy', 'char_porosity', 'mean_pore_radius',
         'specific_internal_surface_area', 'tortuosity', 'burning_mode']

    _child_classes = dict(
        diffusion_rate_constant=diffusion_rate_constant_cls,
        pre_exponential_factor=pre_exponential_factor_cls,
        activation_energy=activation_energy_cls,
        char_porosity=char_porosity_cls,
        mean_pore_radius=mean_pore_radius_cls,
        specific_internal_surface_area=specific_internal_surface_area_cls,
        tortuosity=tortuosity_cls,
        burning_mode=burning_mode_cls,
    )

