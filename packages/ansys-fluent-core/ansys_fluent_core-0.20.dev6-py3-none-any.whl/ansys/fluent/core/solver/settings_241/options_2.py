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

from .inlet_diffusion_1 import inlet_diffusion as inlet_diffusion_cls
from .thermal_diffusion import thermal_diffusion as thermal_diffusion_cls
from .thickened_flame_model import thickened_flame_model as thickened_flame_model_cls
from .diffusion_energy_source import diffusion_energy_source as diffusion_energy_source_cls
from .multi_component_diffusion_mf import multi_component_diffusion_mf as multi_component_diffusion_mf_cls
from .multi_component_diffusion import multi_component_diffusion as multi_component_diffusion_cls
from .liquid_energy_diffusion import liquid_energy_diffusion as liquid_energy_diffusion_cls
from .save_gradients import save_gradients as save_gradients_cls
from .species_migration import species_migration as species_migration_cls
from .species_transport_expert import species_transport_expert as species_transport_expert_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['inlet_diffusion', 'thermal_diffusion', 'thickened_flame_model',
         'diffusion_energy_source', 'multi_component_diffusion_mf',
         'multi_component_diffusion', 'liquid_energy_diffusion',
         'save_gradients', 'species_migration', 'species_transport_expert']

    _child_classes = dict(
        inlet_diffusion=inlet_diffusion_cls,
        thermal_diffusion=thermal_diffusion_cls,
        thickened_flame_model=thickened_flame_model_cls,
        diffusion_energy_source=diffusion_energy_source_cls,
        multi_component_diffusion_mf=multi_component_diffusion_mf_cls,
        multi_component_diffusion=multi_component_diffusion_cls,
        liquid_energy_diffusion=liquid_energy_diffusion_cls,
        save_gradients=save_gradients_cls,
        species_migration=species_migration_cls,
        species_transport_expert=species_transport_expert_cls,
    )

