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

from .day import day as day_cls
from .month import month as month_cls
from .hour import hour as hour_cls
from .minute import minute as minute_cls
class date_and_time(Group):
    """
    'date_and_time' child.
    """

    fluent_name = "date-and-time"

    child_names = \
        ['day', 'month', 'hour', 'minute']

    _child_classes = dict(
        day=day_cls,
        month=month_cls,
        hour=hour_cls,
        minute=minute_cls,
    )

