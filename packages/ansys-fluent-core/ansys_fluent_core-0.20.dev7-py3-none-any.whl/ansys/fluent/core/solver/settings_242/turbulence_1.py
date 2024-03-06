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

from .number_of_vortices import number_of_vortices as number_of_vortices_cls
from .include_streamwise_fluctuations import include_streamwise_fluctuations as include_streamwise_fluctuations_cls
from .satisfy_mass_conservation import satisfy_mass_conservation as satisfy_mass_conservation_cls
from .scale_search_limiter import scale_search_limiter as scale_search_limiter_cls
from .turbulent_intensity_perc import turbulent_intensity_perc as turbulent_intensity_perc_cls
from .turbulent_viscosity_ratio_stg import turbulent_viscosity_ratio_stg as turbulent_viscosity_ratio_stg_cls
from .wall_distance import wall_distance as wall_distance_cls
from .volumetric_forcing import volumetric_forcing as volumetric_forcing_cls
from .forcing_zone_thickness import forcing_zone_thickness as forcing_zone_thickness_cls
from .volumetric_thickness import volumetric_thickness as volumetric_thickness_cls
from .les_spec import les_spec as les_spec_cls
from .fluctuating_velocity_algorithm import fluctuating_velocity_algorithm as fluctuating_velocity_algorithm_cls
from .turbulent_specification import turbulent_specification as turbulent_specification_cls
from .modified_turbulent_viscosity_1 import modified_turbulent_viscosity as modified_turbulent_viscosity_cls
from .laminar_kinetic_energy_1 import laminar_kinetic_energy as laminar_kinetic_energy_cls
from .intermittency_1 import intermittency as intermittency_cls
from .turbulent_kinetic_energy_1 import turbulent_kinetic_energy as turbulent_kinetic_energy_cls
from .turbulent_dissipation_rate_1 import turbulent_dissipation_rate as turbulent_dissipation_rate_cls
from .specific_dissipation_rate_1 import specific_dissipation_rate as specific_dissipation_rate_cls
from .velocity_variance_scale_1 import velocity_variance_scale as velocity_variance_scale_cls
from .turbulent_intensity_1 import turbulent_intensity as turbulent_intensity_cls
from .turbulent_length_scale_1 import turbulent_length_scale as turbulent_length_scale_cls
from .hydraulic_diameter_1 import hydraulic_diameter as hydraulic_diameter_cls
from .turbulent_viscosity_ratio_1 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .turbulent_viscosity_ratio_profile_1 import turbulent_viscosity_ratio_profile as turbulent_viscosity_ratio_profile_cls
from .subgrid_kinetic_energy_specification import subgrid_kinetic_energy_specification as subgrid_kinetic_energy_specification_cls
from .subgrid_kinetic_energy import subgrid_kinetic_energy as subgrid_kinetic_energy_cls
from .subgrid_turbulent_intensity import subgrid_turbulent_intensity as subgrid_turbulent_intensity_cls
from .number_of_fourier_modes import number_of_fourier_modes as number_of_fourier_modes_cls
from .reynolds_stress_specification import reynolds_stress_specification as reynolds_stress_specification_cls
from .uu_reynolds_stresses_1 import uu_reynolds_stresses as uu_reynolds_stresses_cls
from .vv_reynolds_stresses_1 import vv_reynolds_stresses as vv_reynolds_stresses_cls
from .ww_reynolds_stresses_1 import ww_reynolds_stresses as ww_reynolds_stresses_cls
from .uv_reynolds_stresses_1 import uv_reynolds_stresses as uv_reynolds_stresses_cls
from .vw_reynolds_stresses_1 import vw_reynolds_stresses as vw_reynolds_stresses_cls
from .uw_reynolds_stresses_1 import uw_reynolds_stresses as uw_reynolds_stresses_cls
class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['number_of_vortices', 'include_streamwise_fluctuations',
         'satisfy_mass_conservation', 'scale_search_limiter',
         'turbulent_intensity_perc', 'turbulent_viscosity_ratio_stg',
         'wall_distance', 'volumetric_forcing', 'forcing_zone_thickness',
         'volumetric_thickness', 'les_spec', 'fluctuating_velocity_algorithm',
         'turbulent_specification', 'modified_turbulent_viscosity',
         'laminar_kinetic_energy', 'intermittency',
         'turbulent_kinetic_energy', 'turbulent_dissipation_rate',
         'specific_dissipation_rate', 'velocity_variance_scale',
         'turbulent_intensity', 'turbulent_length_scale',
         'hydraulic_diameter', 'turbulent_viscosity_ratio',
         'turbulent_viscosity_ratio_profile',
         'subgrid_kinetic_energy_specification', 'subgrid_kinetic_energy',
         'subgrid_turbulent_intensity', 'number_of_fourier_modes',
         'reynolds_stress_specification', 'uu_reynolds_stresses',
         'vv_reynolds_stresses', 'ww_reynolds_stresses',
         'uv_reynolds_stresses', 'vw_reynolds_stresses',
         'uw_reynolds_stresses']

    _child_classes = dict(
        number_of_vortices=number_of_vortices_cls,
        include_streamwise_fluctuations=include_streamwise_fluctuations_cls,
        satisfy_mass_conservation=satisfy_mass_conservation_cls,
        scale_search_limiter=scale_search_limiter_cls,
        turbulent_intensity_perc=turbulent_intensity_perc_cls,
        turbulent_viscosity_ratio_stg=turbulent_viscosity_ratio_stg_cls,
        wall_distance=wall_distance_cls,
        volumetric_forcing=volumetric_forcing_cls,
        forcing_zone_thickness=forcing_zone_thickness_cls,
        volumetric_thickness=volumetric_thickness_cls,
        les_spec=les_spec_cls,
        fluctuating_velocity_algorithm=fluctuating_velocity_algorithm_cls,
        turbulent_specification=turbulent_specification_cls,
        modified_turbulent_viscosity=modified_turbulent_viscosity_cls,
        laminar_kinetic_energy=laminar_kinetic_energy_cls,
        intermittency=intermittency_cls,
        turbulent_kinetic_energy=turbulent_kinetic_energy_cls,
        turbulent_dissipation_rate=turbulent_dissipation_rate_cls,
        specific_dissipation_rate=specific_dissipation_rate_cls,
        velocity_variance_scale=velocity_variance_scale_cls,
        turbulent_intensity=turbulent_intensity_cls,
        turbulent_length_scale=turbulent_length_scale_cls,
        hydraulic_diameter=hydraulic_diameter_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
        turbulent_viscosity_ratio_profile=turbulent_viscosity_ratio_profile_cls,
        subgrid_kinetic_energy_specification=subgrid_kinetic_energy_specification_cls,
        subgrid_kinetic_energy=subgrid_kinetic_energy_cls,
        subgrid_turbulent_intensity=subgrid_turbulent_intensity_cls,
        number_of_fourier_modes=number_of_fourier_modes_cls,
        reynolds_stress_specification=reynolds_stress_specification_cls,
        uu_reynolds_stresses=uu_reynolds_stresses_cls,
        vv_reynolds_stresses=vv_reynolds_stresses_cls,
        ww_reynolds_stresses=ww_reynolds_stresses_cls,
        uv_reynolds_stresses=uv_reynolds_stresses_cls,
        vw_reynolds_stresses=vw_reynolds_stresses_cls,
        uw_reynolds_stresses=uw_reynolds_stresses_cls,
    )

