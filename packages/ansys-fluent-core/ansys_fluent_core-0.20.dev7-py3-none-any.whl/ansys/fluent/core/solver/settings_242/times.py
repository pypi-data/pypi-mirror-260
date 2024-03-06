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

from .start_time import start_time as start_time_cls
from .stop_time import stop_time as stop_time_cls
class times(Group):
    """
    'times' child.
    """

    fluent_name = "times"

    child_names = \
        ['start_time', 'stop_time']

    _child_classes = dict(
        start_time=start_time_cls,
        stop_time=stop_time_cls,
    )

