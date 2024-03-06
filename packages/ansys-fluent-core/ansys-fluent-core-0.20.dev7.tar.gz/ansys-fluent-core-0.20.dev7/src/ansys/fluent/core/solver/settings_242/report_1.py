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

from .electrolyte_area import electrolyte_area as electrolyte_area_cls
from .monitor_enable import monitor_enable as monitor_enable_cls
from .monitor_frequency import monitor_frequency as monitor_frequency_cls
class report(Group):
    """
    Report settings.
    """

    fluent_name = "report"

    child_names = \
        ['electrolyte_area', 'monitor_enable', 'monitor_frequency']

    _child_classes = dict(
        electrolyte_area=electrolyte_area_cls,
        monitor_enable=monitor_enable_cls,
        monitor_frequency=monitor_frequency_cls,
    )

