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

from .system_coupling_1 import system_coupling as system_coupling_cls
from .frame_of_reference import frame_of_reference as frame_of_reference_cls
from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .p_profile_multiplier import p_profile_multiplier as p_profile_multiplier_cls
from .direction_spec import direction_spec as direction_spec_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .p_backflow_spec_gen import p_backflow_spec_gen as p_backflow_spec_gen_cls
from .p_backflow_spec import p_backflow_spec as p_backflow_spec_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .prevent_reverse_flow import prevent_reverse_flow as prevent_reverse_flow_cls
from .radial import radial as radial_cls
from .avg_press_spec import avg_press_spec as avg_press_spec_cls
from .press_averaging_method import press_averaging_method as press_averaging_method_cls
from .targeted_mf_boundary import targeted_mf_boundary as targeted_mf_boundary_cls
from .targeted_mf import targeted_mf as targeted_mf_cls
from .targeted_mf_pmax import targeted_mf_pmax as targeted_mf_pmax_cls
from .targeted_mf_pmin import targeted_mf_pmin as targeted_mf_pmin_cls
from .gen_nrbc_spec import gen_nrbc_spec as gen_nrbc_spec_cls
from .ac_options import ac_options as ac_options_cls
from .impedance_0 import impedance_0 as impedance_0_cls
from .impedance_1 import impedance_1 as impedance_1_cls
from .impedance_2 import impedance_2 as impedance_2_cls
from .ac_wave import ac_wave as ac_wave_cls
from .pressure_jump import pressure_jump as pressure_jump_cls
from .strength import strength as strength_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['system_coupling', 'frame_of_reference', 'gauge_pressure',
         'p_profile_multiplier', 'direction_spec', 'coordinate_system',
         'flow_direction', 'p_backflow_spec_gen', 'p_backflow_spec',
         'axis_direction', 'axis_origin', 'prevent_reverse_flow', 'radial',
         'avg_press_spec', 'press_averaging_method', 'targeted_mf_boundary',
         'targeted_mf', 'targeted_mf_pmax', 'targeted_mf_pmin',
         'gen_nrbc_spec', 'ac_options', 'impedance_0', 'impedance_1',
         'impedance_2', 'ac_wave', 'pressure_jump', 'strength',
         'new_fan_definition']

    _child_classes = dict(
        system_coupling=system_coupling_cls,
        frame_of_reference=frame_of_reference_cls,
        gauge_pressure=gauge_pressure_cls,
        p_profile_multiplier=p_profile_multiplier_cls,
        direction_spec=direction_spec_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        p_backflow_spec_gen=p_backflow_spec_gen_cls,
        p_backflow_spec=p_backflow_spec_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        prevent_reverse_flow=prevent_reverse_flow_cls,
        radial=radial_cls,
        avg_press_spec=avg_press_spec_cls,
        press_averaging_method=press_averaging_method_cls,
        targeted_mf_boundary=targeted_mf_boundary_cls,
        targeted_mf=targeted_mf_cls,
        targeted_mf_pmax=targeted_mf_pmax_cls,
        targeted_mf_pmin=targeted_mf_pmin_cls,
        gen_nrbc_spec=gen_nrbc_spec_cls,
        ac_options=ac_options_cls,
        impedance_0=impedance_0_cls,
        impedance_1=impedance_1_cls,
        impedance_2=impedance_2_cls,
        ac_wave=ac_wave_cls,
        pressure_jump=pressure_jump_cls,
        strength=strength_cls,
        new_fan_definition=new_fan_definition_cls,
    )

