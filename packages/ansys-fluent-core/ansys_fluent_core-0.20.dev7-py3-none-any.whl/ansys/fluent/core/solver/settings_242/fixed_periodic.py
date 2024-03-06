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

from .enabled_38 import enabled as enabled_cls
from .fixed_periodic_type import fixed_periodic_type as fixed_periodic_type_cls
from .period import period as period_cls
from .times_steps_per_period import times_steps_per_period as times_steps_per_period_cls
from .total_periods import total_periods as total_periods_cls
class fixed_periodic(Group):
    """
    Set period- or frequency-based fixed time-stepping parameters.
    """

    fluent_name = "fixed-periodic"

    child_names = \
        ['enabled', 'fixed_periodic_type', 'period', 'times_steps_per_period',
         'total_periods']

    _child_classes = dict(
        enabled=enabled_cls,
        fixed_periodic_type=fixed_periodic_type_cls,
        period=period_cls,
        times_steps_per_period=times_steps_per_period_cls,
        total_periods=total_periods_cls,
    )

