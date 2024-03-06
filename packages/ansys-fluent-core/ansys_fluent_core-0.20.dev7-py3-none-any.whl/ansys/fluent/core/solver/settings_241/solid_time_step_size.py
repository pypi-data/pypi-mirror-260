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

from .enable_solid_time_step import enable_solid_time_step as enable_solid_time_step_cls
from .choose_auto_time_stepping import choose_auto_time_stepping as choose_auto_time_stepping_cls
from .time_step_size_1 import time_step_size as time_step_size_cls
class solid_time_step_size(Group):
    """
    Enter time step size settings menu for solid zones.
    """

    fluent_name = "solid-time-step-size"

    child_names = \
        ['enable_solid_time_step', 'choose_auto_time_stepping',
         'time_step_size']

    _child_classes = dict(
        enable_solid_time_step=enable_solid_time_step_cls,
        choose_auto_time_stepping=choose_auto_time_stepping_cls,
        time_step_size=time_step_size_cls,
    )

