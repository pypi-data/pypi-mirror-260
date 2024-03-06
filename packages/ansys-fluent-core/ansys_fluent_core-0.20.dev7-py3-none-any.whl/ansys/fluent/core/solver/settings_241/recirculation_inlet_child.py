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

from .name import name as name_cls
from .phase_22 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .outlet_zone import outlet_zone as outlet_zone_cls
from .temperature_rise_specification import temperature_rise_specification as temperature_rise_specification_cls
from .temperature_rise import temperature_rise as temperature_rise_cls
from .heat_source import heat_source as heat_source_cls
from .freestream_temperature import freestream_temperature as freestream_temperature_cls
from .transfer_coefficient import transfer_coefficient as transfer_coefficient_cls
from .direction_specification import direction_specification as direction_specification_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
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
from .turbulent_viscosity_ratio_real_1 import turbulent_viscosity_ratio_real as turbulent_viscosity_ratio_real_cls
from .turbulent_viscosity_ratio_1 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .reynolds_stress_specification import reynolds_stress_specification as reynolds_stress_specification_cls
from .uu_reynolds_stresses_1 import uu_reynolds_stresses as uu_reynolds_stresses_cls
from .vv_reynolds_stresses_1 import vv_reynolds_stresses as vv_reynolds_stresses_cls
from .ww_reynolds_stresses_1 import ww_reynolds_stresses as ww_reynolds_stresses_cls
from .uv_reynolds_stresses_1 import uv_reynolds_stresses as uv_reynolds_stresses_cls
from .vw_reynolds_stresses_1 import vw_reynolds_stresses as vw_reynolds_stresses_cls
from .uw_reynolds_stresses_1 import uw_reynolds_stresses as uw_reynolds_stresses_cls
from .subgrid_kinetic_energy_specification import subgrid_kinetic_energy_specification as subgrid_kinetic_energy_specification_cls
from .subgrid_kinetic_energy import subgrid_kinetic_energy as subgrid_kinetic_energy_cls
from .subgrid_turbulent_intensity import subgrid_turbulent_intensity as subgrid_turbulent_intensity_cls
from .mass_flow_multiplier import mass_flow_multiplier as mass_flow_multiplier_cls
from .participates_in_solar_ray_tracing import participates_in_solar_ray_tracing as participates_in_solar_ray_tracing_cls
from .solar_transmissivity_factor import solar_transmissivity_factor as solar_transmissivity_factor_cls
class recirculation_inlet_child(Group):
    """
    'child_object_type' of recirculation_inlet.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x',
         'geom_dir_y', 'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'outlet_zone', 'temperature_rise_specification', 'temperature_rise',
         'heat_source', 'freestream_temperature', 'transfer_coefficient',
         'direction_specification', 'coordinate_system', 'flow_direction',
         'direction_vector', 'turbulent_specification',
         'modified_turbulent_viscosity', 'laminar_kinetic_energy',
         'intermittency', 'turbulent_kinetic_energy',
         'turbulent_dissipation_rate', 'specific_dissipation_rate',
         'velocity_variance_scale', 'turbulent_intensity',
         'turbulent_length_scale', 'hydraulic_diameter',
         'turbulent_viscosity_ratio_real', 'turbulent_viscosity_ratio',
         'reynolds_stress_specification', 'uu_reynolds_stresses',
         'vv_reynolds_stresses', 'ww_reynolds_stresses',
         'uv_reynolds_stresses', 'vw_reynolds_stresses',
         'uw_reynolds_stresses', 'subgrid_kinetic_energy_specification',
         'subgrid_kinetic_energy', 'subgrid_turbulent_intensity',
         'mass_flow_multiplier', 'participates_in_solar_ray_tracing',
         'solar_transmissivity_factor']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        geom_disable=geom_disable_cls,
        geom_dir_spec=geom_dir_spec_cls,
        geom_dir_x=geom_dir_x_cls,
        geom_dir_y=geom_dir_y_cls,
        geom_dir_z=geom_dir_z_cls,
        geom_levels=geom_levels_cls,
        geom_bgthread=geom_bgthread_cls,
        outlet_zone=outlet_zone_cls,
        temperature_rise_specification=temperature_rise_specification_cls,
        temperature_rise=temperature_rise_cls,
        heat_source=heat_source_cls,
        freestream_temperature=freestream_temperature_cls,
        transfer_coefficient=transfer_coefficient_cls,
        direction_specification=direction_specification_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
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
        turbulent_viscosity_ratio_real=turbulent_viscosity_ratio_real_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
        reynolds_stress_specification=reynolds_stress_specification_cls,
        uu_reynolds_stresses=uu_reynolds_stresses_cls,
        vv_reynolds_stresses=vv_reynolds_stresses_cls,
        ww_reynolds_stresses=ww_reynolds_stresses_cls,
        uv_reynolds_stresses=uv_reynolds_stresses_cls,
        vw_reynolds_stresses=vw_reynolds_stresses_cls,
        uw_reynolds_stresses=uw_reynolds_stresses_cls,
        subgrid_kinetic_energy_specification=subgrid_kinetic_energy_specification_cls,
        subgrid_kinetic_energy=subgrid_kinetic_energy_cls,
        subgrid_turbulent_intensity=subgrid_turbulent_intensity_cls,
        mass_flow_multiplier=mass_flow_multiplier_cls,
        participates_in_solar_ray_tracing=participates_in_solar_ray_tracing_cls,
        solar_transmissivity_factor=solar_transmissivity_factor_cls,
    )

