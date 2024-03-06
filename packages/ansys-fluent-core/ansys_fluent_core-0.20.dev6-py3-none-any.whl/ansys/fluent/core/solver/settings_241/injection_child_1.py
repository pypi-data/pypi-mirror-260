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
from .report_type import report_type as report_type_cls
from .injection_list import injection_list as injection_list_cls
from .boundaries_1 import boundaries as boundaries_cls
from .physics_1 import physics as physics_cls
from .per_injection import per_injection as per_injection_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .mass_criterion import mass_criterion as mass_criterion_cls
from .user_specified_origin_and_axis import user_specified_origin_and_axis as user_specified_origin_and_axis_cls
from .origin import origin as origin_cls
from .axis import axis as axis_cls
from .show_unsteady_rate import show_unsteady_rate as show_unsteady_rate_cls
from .inj_mass_rate_prev_time import inj_mass_rate_prev_time as inj_mass_rate_prev_time_cls
from .inj_mass_rate_prev_mass import inj_mass_rate_prev_mass as inj_mass_rate_prev_mass_cls
from .inj_mass_rate_last_flow import inj_mass_rate_last_flow as inj_mass_rate_last_flow_cls
from .inj_mass_rate_last_tstp import inj_mass_rate_last_tstp as inj_mass_rate_last_tstp_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class injection_child(Group):
    """
    'child_object_type' of injection.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'injection_list', 'boundaries', 'physics',
         'per_injection', 'average_over', 'retain_instantaneous_values',
         'mass_criterion', 'user_specified_origin_and_axis', 'origin', 'axis',
         'show_unsteady_rate', 'inj_mass_rate_prev_time',
         'inj_mass_rate_prev_mass', 'inj_mass_rate_last_flow',
         'inj_mass_rate_last_tstp']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        injection_list=injection_list_cls,
        boundaries=boundaries_cls,
        physics=physics_cls,
        per_injection=per_injection_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        mass_criterion=mass_criterion_cls,
        user_specified_origin_and_axis=user_specified_origin_and_axis_cls,
        origin=origin_cls,
        axis=axis_cls,
        show_unsteady_rate=show_unsteady_rate_cls,
        inj_mass_rate_prev_time=inj_mass_rate_prev_time_cls,
        inj_mass_rate_prev_mass=inj_mass_rate_prev_mass_cls,
        inj_mass_rate_last_flow=inj_mass_rate_last_flow_cls,
        inj_mass_rate_last_tstp=inj_mass_rate_last_tstp_cls,
        create_output_parameter=create_output_parameter_cls,
    )

