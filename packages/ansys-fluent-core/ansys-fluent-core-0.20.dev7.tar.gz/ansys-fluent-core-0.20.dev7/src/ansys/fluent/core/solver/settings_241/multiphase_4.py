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

from .open_channel_1 import open_channel as open_channel_cls
from .inlet_number import inlet_number as inlet_number_cls
from .secondary_phase_for_inlet import secondary_phase_for_inlet as secondary_phase_for_inlet_cls
from .free_surface_level import free_surface_level as free_surface_level_cls
from .bottom_level import bottom_level as bottom_level_cls
from .density_interpolation_method import density_interpolation_method as density_interpolation_method_cls
from .pb_disc_bc import pb_disc_bc as pb_disc_bc_cls
from .pb_disc import pb_disc as pb_disc_cls
from .pb_qmom_bc import pb_qmom_bc as pb_qmom_bc_cls
from .pb_qmom import pb_qmom as pb_qmom_cls
from .pb_qbmm_bc import pb_qbmm_bc as pb_qbmm_bc_cls
from .pb_qbmm import pb_qbmm as pb_qbmm_cls
from .pb_smm_bc import pb_smm_bc as pb_smm_bc_cls
from .pb_smm import pb_smm as pb_smm_cls
from .pb_dqmom_bc import pb_dqmom_bc as pb_dqmom_bc_cls
from .pb_dqmom import pb_dqmom as pb_dqmom_cls
from .slip_velocity_specification import slip_velocity_specification as slip_velocity_specification_cls
from .phase_velocity_ratio import phase_velocity_ratio as phase_velocity_ratio_cls
from .volume_fraction_1 import volume_fraction as volume_fraction_cls
from .granular_temperature_1 import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration_1 import interfacial_area_concentration as interfacial_area_concentration_cls
from .relative_humidity import relative_humidity as relative_humidity_cls
from .liquid_mass_fraction import liquid_mass_fraction as liquid_mass_fraction_cls
from .log10_droplets_per_unit_volume import log10_droplets_per_unit_volume as log10_droplets_per_unit_volume_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel', 'inlet_number', 'secondary_phase_for_inlet',
         'free_surface_level', 'bottom_level', 'density_interpolation_method',
         'pb_disc_bc', 'pb_disc', 'pb_qmom_bc', 'pb_qmom', 'pb_qbmm_bc',
         'pb_qbmm', 'pb_smm_bc', 'pb_smm', 'pb_dqmom_bc', 'pb_dqmom',
         'slip_velocity_specification', 'phase_velocity_ratio',
         'volume_fraction', 'granular_temperature',
         'interfacial_area_concentration', 'relative_humidity',
         'liquid_mass_fraction', 'log10_droplets_per_unit_volume']

    _child_classes = dict(
        open_channel=open_channel_cls,
        inlet_number=inlet_number_cls,
        secondary_phase_for_inlet=secondary_phase_for_inlet_cls,
        free_surface_level=free_surface_level_cls,
        bottom_level=bottom_level_cls,
        density_interpolation_method=density_interpolation_method_cls,
        pb_disc_bc=pb_disc_bc_cls,
        pb_disc=pb_disc_cls,
        pb_qmom_bc=pb_qmom_bc_cls,
        pb_qmom=pb_qmom_cls,
        pb_qbmm_bc=pb_qbmm_bc_cls,
        pb_qbmm=pb_qbmm_cls,
        pb_smm_bc=pb_smm_bc_cls,
        pb_smm=pb_smm_cls,
        pb_dqmom_bc=pb_dqmom_bc_cls,
        pb_dqmom=pb_dqmom_cls,
        slip_velocity_specification=slip_velocity_specification_cls,
        phase_velocity_ratio=phase_velocity_ratio_cls,
        volume_fraction=volume_fraction_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        relative_humidity=relative_humidity_cls,
        liquid_mass_fraction=liquid_mass_fraction_cls,
        log10_droplets_per_unit_volume=log10_droplets_per_unit_volume_cls,
    )

