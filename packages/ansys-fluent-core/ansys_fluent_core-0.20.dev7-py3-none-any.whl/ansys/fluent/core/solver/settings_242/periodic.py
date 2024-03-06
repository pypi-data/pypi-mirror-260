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

from .rotationally_periodic import rotationally_periodic as rotationally_periodic_cls
from .p_jump import p_jump as p_jump_cls
from .axis_direction_3 import axis_direction as axis_direction_cls
from .axis_origin_3 import axis_origin as axis_origin_cls
from .shift_component import shift_component as shift_component_cls
from .per_angle import per_angle as per_angle_cls
class periodic(Group):
    """
    Help not available.
    """

    fluent_name = "periodic"

    child_names = \
        ['rotationally_periodic', 'p_jump', 'axis_direction', 'axis_origin',
         'shift_component', 'per_angle']

    _child_classes = dict(
        rotationally_periodic=rotationally_periodic_cls,
        p_jump=p_jump_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        shift_component=shift_component_cls,
        per_angle=per_angle_cls,
    )

