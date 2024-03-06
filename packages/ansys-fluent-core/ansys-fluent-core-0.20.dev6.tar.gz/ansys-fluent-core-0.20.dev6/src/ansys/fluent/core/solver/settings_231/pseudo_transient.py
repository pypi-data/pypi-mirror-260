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

from .smoothed_density_stabilization_method import smoothed_density_stabilization_method as smoothed_density_stabilization_method_cls
from .num_of_density_smoothing import num_of_density_smoothing as num_of_density_smoothing_cls
from .false_time_step_linearization import false_time_step_linearization as false_time_step_linearization_cls
from .auto_dt_advanced_controls import auto_dt_advanced_controls as auto_dt_advanced_controls_cls
class pseudo_transient(Group):
    """
    Pseudo-Time stability controls for multiphase flow.
    """

    fluent_name = "pseudo-transient"

    child_names = \
        ['smoothed_density_stabilization_method', 'num_of_density_smoothing',
         'false_time_step_linearization', 'auto_dt_advanced_controls']

    _child_classes = dict(
        smoothed_density_stabilization_method=smoothed_density_stabilization_method_cls,
        num_of_density_smoothing=num_of_density_smoothing_cls,
        false_time_step_linearization=false_time_step_linearization_cls,
        auto_dt_advanced_controls=auto_dt_advanced_controls_cls,
    )

