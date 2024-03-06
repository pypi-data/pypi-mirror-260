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
from .gauge_total_pressure import gauge_total_pressure as gauge_total_pressure_cls
from .supersonic_or_initial_gauge_pressure import supersonic_or_initial_gauge_pressure as supersonic_or_initial_gauge_pressure_cls
from .direction_specification_method import direction_specification_method as direction_specification_method_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .prevent_reverse_flow import prevent_reverse_flow as prevent_reverse_flow_cls
from .ac_options import ac_options as ac_options_cls
from .impedance_0 import impedance_0 as impedance_0_cls
from .impedance_1 import impedance_1 as impedance_1_cls
from .impedance_2 import impedance_2 as impedance_2_cls
from .ac_wave import ac_wave as ac_wave_cls
from .pressure_jump import pressure_jump as pressure_jump_cls
from .swirl_velocity_specification import swirl_velocity_specification as swirl_velocity_specification_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
from .fan_rotation_speed import fan_rotation_speed as fan_rotation_speed_cls
from .fan_origin import fan_origin as fan_origin_cls
from .strength import strength as strength_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['reference_frame', 'gauge_total_pressure',
         'supersonic_or_initial_gauge_pressure',
         'direction_specification_method', 'coordinate_system',
         'flow_direction', 'direction_vector', 'axis_direction',
         'axis_origin', 'prevent_reverse_flow', 'ac_options', 'impedance_0',
         'impedance_1', 'impedance_2', 'ac_wave', 'pressure_jump',
         'swirl_velocity_specification', 'swirl_factor', 'fan_rotation_speed',
         'fan_origin', 'strength', 'new_fan_definition']

    _child_classes = dict(
        reference_frame=reference_frame_cls,
        gauge_total_pressure=gauge_total_pressure_cls,
        supersonic_or_initial_gauge_pressure=supersonic_or_initial_gauge_pressure_cls,
        direction_specification_method=direction_specification_method_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        prevent_reverse_flow=prevent_reverse_flow_cls,
        ac_options=ac_options_cls,
        impedance_0=impedance_0_cls,
        impedance_1=impedance_1_cls,
        impedance_2=impedance_2_cls,
        ac_wave=ac_wave_cls,
        pressure_jump=pressure_jump_cls,
        swirl_velocity_specification=swirl_velocity_specification_cls,
        swirl_factor=swirl_factor_cls,
        fan_rotation_speed=fan_rotation_speed_cls,
        fan_origin=fan_origin_cls,
        strength=strength_cls,
        new_fan_definition=new_fan_definition_cls,
    )

