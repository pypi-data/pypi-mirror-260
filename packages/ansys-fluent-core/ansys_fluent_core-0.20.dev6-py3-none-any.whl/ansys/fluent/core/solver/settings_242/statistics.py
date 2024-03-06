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

from .reset_statistics import reset_statistics as reset_statistics_cls
from .statistics_controls import statistics_controls as statistics_controls_cls
class statistics(Group):
    """
    Enter the statistics menu, where you can set up the sampling of the fluid density field during the calculation.
    """

    fluent_name = "statistics"

    child_names = \
        ['reset_statistics']

    command_names = \
        ['statistics_controls']

    _child_classes = dict(
        reset_statistics=reset_statistics_cls,
        statistics_controls=statistics_controls_cls,
    )

