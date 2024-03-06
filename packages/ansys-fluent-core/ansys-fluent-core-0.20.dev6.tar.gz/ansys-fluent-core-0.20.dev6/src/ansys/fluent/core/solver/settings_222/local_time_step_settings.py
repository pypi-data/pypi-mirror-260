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

from .pseudo_time_courant_number import pseudo_time_courant_number as pseudo_time_courant_number_cls
from .pseudo_time_step_method_solid_zone import pseudo_time_step_method_solid_zone as pseudo_time_step_method_solid_zone_cls
from .time_step_size_scale_factor import time_step_size_scale_factor as time_step_size_scale_factor_cls
class local_time_step_settings(Group):
    """
    'local_time_step_settings' child.
    """

    fluent_name = "local-time-step-settings"

    child_names = \
        ['pseudo_time_courant_number', 'pseudo_time_step_method_solid_zone',
         'time_step_size_scale_factor']

    _child_classes = dict(
        pseudo_time_courant_number=pseudo_time_courant_number_cls,
        pseudo_time_step_method_solid_zone=pseudo_time_step_method_solid_zone_cls,
        time_step_size_scale_factor=time_step_size_scale_factor_cls,
    )

