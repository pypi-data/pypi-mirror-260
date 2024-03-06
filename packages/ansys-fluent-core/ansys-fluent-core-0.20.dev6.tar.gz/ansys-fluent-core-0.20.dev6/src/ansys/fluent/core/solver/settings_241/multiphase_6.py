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

from .open_channel_wave_bc import open_channel_wave_bc as open_channel_wave_bc_cls
from .segregated_velocity_inputs import segregated_velocity_inputs as segregated_velocity_inputs_cls
from .averaged_flow_specification_method import averaged_flow_specification_method as averaged_flow_specification_method_cls
from .avg_flow_velocity import avg_flow_velocity as avg_flow_velocity_cls
from .wave_velocity import wave_velocity as wave_velocity_cls
from .moving_object_velocity_specification_method import moving_object_velocity_specification_method as moving_object_velocity_specification_method_cls
from .moving_object_velocity import moving_object_velocity as moving_object_velocity_cls
from .moving_object_direction import moving_object_direction as moving_object_direction_cls
from .secondary_phase_velocity_specification_method import secondary_phase_velocity_specification_method as secondary_phase_velocity_specification_method_cls
from .secondary_phase_velocity import secondary_phase_velocity as secondary_phase_velocity_cls
from .secondary_phase_direction import secondary_phase_direction as secondary_phase_direction_cls
from .primary_phase_velocity_specification_method import primary_phase_velocity_specification_method as primary_phase_velocity_specification_method_cls
from .primary_phase_reference_height_above_free_surface import primary_phase_reference_height_above_free_surface as primary_phase_reference_height_above_free_surface_cls
from .primary_phase_power_law_coefficient import primary_phase_power_law_coefficient as primary_phase_power_law_coefficient_cls
from .primary_phase_velocity import primary_phase_velocity as primary_phase_velocity_cls
from .primary_phase_reference_velocity import primary_phase_reference_velocity as primary_phase_reference_velocity_cls
from .primary_phase_direction import primary_phase_direction as primary_phase_direction_cls
from .secondary_phase_for_inlet import secondary_phase_for_inlet as secondary_phase_for_inlet_cls
from .wave_option import wave_option as wave_option_cls
from .free_surface_level import free_surface_level as free_surface_level_cls
from .bottom_level import bottom_level as bottom_level_cls
from .reference_wave_direction import reference_wave_direction as reference_wave_direction_cls
from .reference_direction import reference_direction as reference_direction_cls
from .wave_modeling_option import wave_modeling_option as wave_modeling_option_cls
from .wave_group_inputs import wave_group_inputs as wave_group_inputs_cls
from .shallow_wave_inputs import shallow_wave_inputs as shallow_wave_inputs_cls
from .frequency_spectrum_method import frequency_spectrum_method as frequency_spectrum_method_cls
from .peak_shape_parameter import peak_shape_parameter as peak_shape_parameter_cls
from .significant_wave_height import significant_wave_height as significant_wave_height_cls
from .peak_frequency import peak_frequency as peak_frequency_cls
from .minimum_frequency import minimum_frequency as minimum_frequency_cls
from .maximum_frequency import maximum_frequency as maximum_frequency_cls
from .number_of_frequency_components import number_of_frequency_components as number_of_frequency_components_cls
from .directional_spreading_method import directional_spreading_method as directional_spreading_method_cls
from .frequency_independent_cosine_exponent import frequency_independent_cosine_exponent as frequency_independent_cosine_exponent_cls
from .mean_wave_heading_angle import mean_wave_heading_angle as mean_wave_heading_angle_cls
from .angular_deviation import angular_deviation as angular_deviation_cls
from .number_of_angular_components import number_of_angular_components as number_of_angular_components_cls
from .granular_temperature_1 import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration_1 import interfacial_area_concentration as interfacial_area_concentration_cls
from .level_set_function_flux_1 import level_set_function_flux as level_set_function_flux_cls
from .volume_fraction_1 import volume_fraction as volume_fraction_cls
from .pb_disc_bc import pb_disc_bc as pb_disc_bc_cls
from .pb_disc_1 import pb_disc as pb_disc_cls
from .pb_qmom_bc import pb_qmom_bc as pb_qmom_bc_cls
from .pb_qmom import pb_qmom as pb_qmom_cls
from .pb_qbmm_bc import pb_qbmm_bc as pb_qbmm_bc_cls
from .pb_qbmm import pb_qbmm as pb_qbmm_cls
from .pb_smm_bc import pb_smm_bc as pb_smm_bc_cls
from .pb_smm import pb_smm as pb_smm_cls
from .pb_dqmom_bc import pb_dqmom_bc as pb_dqmom_bc_cls
from .pb_dqmom import pb_dqmom as pb_dqmom_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel_wave_bc', 'segregated_velocity_inputs',
         'averaged_flow_specification_method', 'avg_flow_velocity',
         'wave_velocity', 'moving_object_velocity_specification_method',
         'moving_object_velocity', 'moving_object_direction',
         'secondary_phase_velocity_specification_method',
         'secondary_phase_velocity', 'secondary_phase_direction',
         'primary_phase_velocity_specification_method',
         'primary_phase_reference_height_above_free_surface',
         'primary_phase_power_law_coefficient', 'primary_phase_velocity',
         'primary_phase_reference_velocity', 'primary_phase_direction',
         'secondary_phase_for_inlet', 'wave_option', 'free_surface_level',
         'bottom_level', 'reference_wave_direction', 'reference_direction',
         'wave_modeling_option', 'wave_group_inputs', 'shallow_wave_inputs',
         'frequency_spectrum_method', 'peak_shape_parameter',
         'significant_wave_height', 'peak_frequency', 'minimum_frequency',
         'maximum_frequency', 'number_of_frequency_components',
         'directional_spreading_method',
         'frequency_independent_cosine_exponent', 'mean_wave_heading_angle',
         'angular_deviation', 'number_of_angular_components',
         'granular_temperature', 'interfacial_area_concentration',
         'level_set_function_flux', 'volume_fraction', 'pb_disc_bc',
         'pb_disc', 'pb_qmom_bc', 'pb_qmom', 'pb_qbmm_bc', 'pb_qbmm',
         'pb_smm_bc', 'pb_smm', 'pb_dqmom_bc', 'pb_dqmom']

    _child_classes = dict(
        open_channel_wave_bc=open_channel_wave_bc_cls,
        segregated_velocity_inputs=segregated_velocity_inputs_cls,
        averaged_flow_specification_method=averaged_flow_specification_method_cls,
        avg_flow_velocity=avg_flow_velocity_cls,
        wave_velocity=wave_velocity_cls,
        moving_object_velocity_specification_method=moving_object_velocity_specification_method_cls,
        moving_object_velocity=moving_object_velocity_cls,
        moving_object_direction=moving_object_direction_cls,
        secondary_phase_velocity_specification_method=secondary_phase_velocity_specification_method_cls,
        secondary_phase_velocity=secondary_phase_velocity_cls,
        secondary_phase_direction=secondary_phase_direction_cls,
        primary_phase_velocity_specification_method=primary_phase_velocity_specification_method_cls,
        primary_phase_reference_height_above_free_surface=primary_phase_reference_height_above_free_surface_cls,
        primary_phase_power_law_coefficient=primary_phase_power_law_coefficient_cls,
        primary_phase_velocity=primary_phase_velocity_cls,
        primary_phase_reference_velocity=primary_phase_reference_velocity_cls,
        primary_phase_direction=primary_phase_direction_cls,
        secondary_phase_for_inlet=secondary_phase_for_inlet_cls,
        wave_option=wave_option_cls,
        free_surface_level=free_surface_level_cls,
        bottom_level=bottom_level_cls,
        reference_wave_direction=reference_wave_direction_cls,
        reference_direction=reference_direction_cls,
        wave_modeling_option=wave_modeling_option_cls,
        wave_group_inputs=wave_group_inputs_cls,
        shallow_wave_inputs=shallow_wave_inputs_cls,
        frequency_spectrum_method=frequency_spectrum_method_cls,
        peak_shape_parameter=peak_shape_parameter_cls,
        significant_wave_height=significant_wave_height_cls,
        peak_frequency=peak_frequency_cls,
        minimum_frequency=minimum_frequency_cls,
        maximum_frequency=maximum_frequency_cls,
        number_of_frequency_components=number_of_frequency_components_cls,
        directional_spreading_method=directional_spreading_method_cls,
        frequency_independent_cosine_exponent=frequency_independent_cosine_exponent_cls,
        mean_wave_heading_angle=mean_wave_heading_angle_cls,
        angular_deviation=angular_deviation_cls,
        number_of_angular_components=number_of_angular_components_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        level_set_function_flux=level_set_function_flux_cls,
        volume_fraction=volume_fraction_cls,
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
    )

