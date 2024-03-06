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

from .node_values import node_values as node_values_cls
from .position_on_x_axis import position_on_x_axis as position_on_x_axis_cls
from .position_on_y_axis import position_on_y_axis as position_on_y_axis_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['node_values', 'position_on_x_axis', 'position_on_y_axis']

    _child_classes = dict(
        node_values=node_values_cls,
        position_on_x_axis=position_on_x_axis_cls,
        position_on_y_axis=position_on_y_axis_cls,
    )

