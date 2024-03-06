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

from .solid_motion import solid_motion as solid_motion_cls
from .solid_relative_to_thread import solid_relative_to_thread as solid_relative_to_thread_cls
from .solid_omega import solid_omega as solid_omega_cls
from .solid_motion_velocity import solid_motion_velocity as solid_motion_velocity_cls
from .solid_motion_axis_origin import solid_motion_axis_origin as solid_motion_axis_origin_cls
from .solid_motion_axis_direction import solid_motion_axis_direction as solid_motion_axis_direction_cls
from .solid_motion_zone_motion_function import solid_motion_zone_motion_function as solid_motion_zone_motion_function_cls
class solid_motion(Group):
    """
    Help not available.
    """

    fluent_name = "solid-motion"

    child_names = \
        ['solid_motion', 'solid_relative_to_thread', 'solid_omega',
         'solid_motion_velocity', 'solid_motion_axis_origin',
         'solid_motion_axis_direction', 'solid_motion_zone_motion_function']

    _child_classes = dict(
        solid_motion=solid_motion_cls,
        solid_relative_to_thread=solid_relative_to_thread_cls,
        solid_omega=solid_omega_cls,
        solid_motion_velocity=solid_motion_velocity_cls,
        solid_motion_axis_origin=solid_motion_axis_origin_cls,
        solid_motion_axis_direction=solid_motion_axis_direction_cls,
        solid_motion_zone_motion_function=solid_motion_zone_motion_function_cls,
    )

