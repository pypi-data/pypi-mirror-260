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

from .auto_time_step_size_cal import auto_time_step_size_cal as auto_time_step_size_cal_cls
from .pseudo_time_step_size import pseudo_time_step_size as pseudo_time_step_size_cls
from .options_length_scale_calc_methods import options_length_scale_calc_methods as options_length_scale_calc_methods_cls
from .auto_time_step_size_scale_factor import auto_time_step_size_scale_factor as auto_time_step_size_scale_factor_cls
from .length_scale import length_scale as length_scale_cls
from .auto_time_size_calc_solid_zone import auto_time_size_calc_solid_zone as auto_time_size_calc_solid_zone_cls
from .auto_time_solid_scale_factor import auto_time_solid_scale_factor as auto_time_solid_scale_factor_cls
from .time_step_size_for_solid_zone import time_step_size_for_solid_zone as time_step_size_for_solid_zone_cls
class global_time_step_settings(Group):
    """
    'global_time_step_settings' child.
    """

    fluent_name = "global-time-step-settings"

    child_names = \
        ['auto_time_step_size_cal', 'pseudo_time_step_size',
         'options_length_scale_calc_methods',
         'auto_time_step_size_scale_factor', 'length_scale',
         'auto_time_size_calc_solid_zone', 'auto_time_solid_scale_factor',
         'time_step_size_for_solid_zone']

    _child_classes = dict(
        auto_time_step_size_cal=auto_time_step_size_cal_cls,
        pseudo_time_step_size=pseudo_time_step_size_cls,
        options_length_scale_calc_methods=options_length_scale_calc_methods_cls,
        auto_time_step_size_scale_factor=auto_time_step_size_scale_factor_cls,
        length_scale=length_scale_cls,
        auto_time_size_calc_solid_zone=auto_time_size_calc_solid_zone_cls,
        auto_time_solid_scale_factor=auto_time_solid_scale_factor_cls,
        time_step_size_for_solid_zone=time_step_size_for_solid_zone_cls,
    )

