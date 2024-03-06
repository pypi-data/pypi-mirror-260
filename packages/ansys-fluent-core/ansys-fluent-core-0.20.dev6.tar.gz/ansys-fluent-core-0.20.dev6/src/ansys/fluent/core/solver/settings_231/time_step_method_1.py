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

from .time_step_method import time_step_method as time_step_method_cls
from .pseudo_time_step_size import pseudo_time_step_size as pseudo_time_step_size_cls
from .length_scale_methods import length_scale_methods as length_scale_methods_cls
from .time_step_size_scale_factor_1 import time_step_size_scale_factor as time_step_size_scale_factor_cls
from .length_scale_1 import length_scale as length_scale_cls
from .auto_time_size_calc_solid_zone import auto_time_size_calc_solid_zone as auto_time_size_calc_solid_zone_cls
from .time_solid_scale_factor import time_solid_scale_factor as time_solid_scale_factor_cls
from .time_step_size_for_solid_zone import time_step_size_for_solid_zone as time_step_size_for_solid_zone_cls
class time_step_method(Group):
    """
    'time_step_method' child.
    """

    fluent_name = "time-step-method"

    child_names = \
        ['time_step_method', 'pseudo_time_step_size', 'length_scale_methods',
         'time_step_size_scale_factor', 'length_scale',
         'auto_time_size_calc_solid_zone', 'time_solid_scale_factor',
         'time_step_size_for_solid_zone']

    _child_classes = dict(
        time_step_method=time_step_method_cls,
        pseudo_time_step_size=pseudo_time_step_size_cls,
        length_scale_methods=length_scale_methods_cls,
        time_step_size_scale_factor=time_step_size_scale_factor_cls,
        length_scale=length_scale_cls,
        auto_time_size_calc_solid_zone=auto_time_size_calc_solid_zone_cls,
        time_solid_scale_factor=time_solid_scale_factor_cls,
        time_step_size_for_solid_zone=time_step_size_for_solid_zone_cls,
    )

