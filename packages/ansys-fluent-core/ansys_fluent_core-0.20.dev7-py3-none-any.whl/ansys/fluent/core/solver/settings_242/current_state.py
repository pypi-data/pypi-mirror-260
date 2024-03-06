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

from .origin_1 import origin as origin_cls
from .x_axis_1 import x_axis as x_axis_cls
from .y_axis_1 import y_axis as y_axis_cls
from .z_axis_1 import z_axis as z_axis_cls
class current_state(Group):
    """
    Current state.
    """

    fluent_name = "current-state"

    child_names = \
        ['origin', 'x_axis', 'y_axis', 'z_axis']

    _child_classes = dict(
        origin=origin_cls,
        x_axis=x_axis_cls,
        y_axis=y_axis_cls,
        z_axis=z_axis_cls,
    )

