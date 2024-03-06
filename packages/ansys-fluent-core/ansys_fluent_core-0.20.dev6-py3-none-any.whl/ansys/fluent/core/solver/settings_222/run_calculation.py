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

from .adaptive_time_stepping import adaptive_time_stepping as adaptive_time_stepping_cls
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping as cfl_based_adaptive_time_stepping_cls
from .data_sampling_1 import data_sampling as data_sampling_cls
from .transient_controls import transient_controls as transient_controls_cls
from .dual_time_iterate import dual_time_iterate as dual_time_iterate_cls
from .iterate import iterate as iterate_cls
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['adaptive_time_stepping', 'cfl_based_adaptive_time_stepping',
         'data_sampling', 'transient_controls']

    command_names = \
        ['dual_time_iterate', 'iterate']

    _child_classes = dict(
        adaptive_time_stepping=adaptive_time_stepping_cls,
        cfl_based_adaptive_time_stepping=cfl_based_adaptive_time_stepping_cls,
        data_sampling=data_sampling_cls,
        transient_controls=transient_controls_cls,
        dual_time_iterate=dual_time_iterate_cls,
        iterate=iterate_cls,
    )

