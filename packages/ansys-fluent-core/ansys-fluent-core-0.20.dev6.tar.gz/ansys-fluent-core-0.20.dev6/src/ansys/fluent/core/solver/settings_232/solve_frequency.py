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

from .method_2 import method as method_cls
from .time_step_interval import time_step_interval as time_step_interval_cls
from .time_interval import time_interval as time_interval_cls
from .iteration_interval import iteration_interval as iteration_interval_cls
class solve_frequency(Group):
    """
    Enter radiation solve frequency.
    """

    fluent_name = "solve-frequency"

    child_names = \
        ['method', 'time_step_interval', 'time_interval',
         'iteration_interval']

    _child_classes = dict(
        method=method_cls,
        time_step_interval=time_step_interval_cls,
        time_interval=time_interval_cls,
        iteration_interval=iteration_interval_cls,
    )

