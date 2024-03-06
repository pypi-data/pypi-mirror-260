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

from .reference_frame_2 import reference_frame as reference_frame_cls
from .mass_flow_specification import mass_flow_specification as mass_flow_specification_cls
from .mass_flow_rate_1 import mass_flow_rate as mass_flow_rate_cls
from .exit_corrected_mass_flow_rate import exit_corrected_mass_flow_rate as exit_corrected_mass_flow_rate_cls
from .mass_flux import mass_flux as mass_flux_cls
from .average_mass_flux import average_mass_flux as average_mass_flux_cls
from .supersonic_gauge_pressure import supersonic_gauge_pressure as supersonic_gauge_pressure_cls
from .direction_specification import direction_specification as direction_specification_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .swirl_velocity_specification import swirl_velocity_specification as swirl_velocity_specification_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
from .fan_origin import fan_origin as fan_origin_cls
from .ecmf_reference_temperature import ecmf_reference_temperature as ecmf_reference_temperature_cls
from .ecmf_reference_gauge_pressure import ecmf_reference_gauge_pressure as ecmf_reference_gauge_pressure_cls
from .ac_options import ac_options as ac_options_cls
from .impedance_0 import impedance_0 as impedance_0_cls
from .impedance_1 import impedance_1 as impedance_1_cls
from .impedance_2 import impedance_2 as impedance_2_cls
from .ac_wave import ac_wave as ac_wave_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['reference_frame', 'mass_flow_specification', 'mass_flow_rate',
         'exit_corrected_mass_flow_rate', 'mass_flux', 'average_mass_flux',
         'supersonic_gauge_pressure', 'direction_specification',
         'coordinate_system', 'flow_direction', 'direction_vector',
         'axis_direction', 'axis_origin', 'swirl_velocity_specification',
         'swirl_factor', 'fan_origin', 'ecmf_reference_temperature',
         'ecmf_reference_gauge_pressure', 'ac_options', 'impedance_0',
         'impedance_1', 'impedance_2', 'ac_wave']

    _child_classes = dict(
        reference_frame=reference_frame_cls,
        mass_flow_specification=mass_flow_specification_cls,
        mass_flow_rate=mass_flow_rate_cls,
        exit_corrected_mass_flow_rate=exit_corrected_mass_flow_rate_cls,
        mass_flux=mass_flux_cls,
        average_mass_flux=average_mass_flux_cls,
        supersonic_gauge_pressure=supersonic_gauge_pressure_cls,
        direction_specification=direction_specification_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        swirl_velocity_specification=swirl_velocity_specification_cls,
        swirl_factor=swirl_factor_cls,
        fan_origin=fan_origin_cls,
        ecmf_reference_temperature=ecmf_reference_temperature_cls,
        ecmf_reference_gauge_pressure=ecmf_reference_gauge_pressure_cls,
        ac_options=ac_options_cls,
        impedance_0=impedance_0_cls,
        impedance_1=impedance_1_cls,
        impedance_2=impedance_2_cls,
        ac_wave=ac_wave_cls,
    )

