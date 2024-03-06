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

from .x_axis_3 import x_axis as x_axis_cls
from .y_axis_3 import y_axis as y_axis_cls
class log_scale(Group):
    """
    'log_scale' child.
    """

    fluent_name = "log-scale"

    child_names = \
        ['x_axis', 'y_axis']

    _child_classes = dict(
        x_axis=x_axis_cls,
        y_axis=y_axis_cls,
    )

