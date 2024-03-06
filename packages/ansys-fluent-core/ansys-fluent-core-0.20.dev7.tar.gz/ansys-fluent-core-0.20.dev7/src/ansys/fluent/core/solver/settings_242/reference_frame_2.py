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

from .frame_motion import frame_motion as frame_motion_cls
from .mrf_relative_to_thread import mrf_relative_to_thread as mrf_relative_to_thread_cls
from .mrf_omega import mrf_omega as mrf_omega_cls
from .reference_frame_velocity import reference_frame_velocity as reference_frame_velocity_cls
from .reference_frame_axis_origin import reference_frame_axis_origin as reference_frame_axis_origin_cls
from .reference_frame_axis_direction import reference_frame_axis_direction as reference_frame_axis_direction_cls
from .reference_frame_zone_motion_function import reference_frame_zone_motion_function as reference_frame_zone_motion_function_cls
class reference_frame(Group):
    """
    Help not available.
    """

    fluent_name = "reference-frame"

    child_names = \
        ['frame_motion', 'mrf_relative_to_thread', 'mrf_omega',
         'reference_frame_velocity', 'reference_frame_axis_origin',
         'reference_frame_axis_direction',
         'reference_frame_zone_motion_function']

    _child_classes = dict(
        frame_motion=frame_motion_cls,
        mrf_relative_to_thread=mrf_relative_to_thread_cls,
        mrf_omega=mrf_omega_cls,
        reference_frame_velocity=reference_frame_velocity_cls,
        reference_frame_axis_origin=reference_frame_axis_origin_cls,
        reference_frame_axis_direction=reference_frame_axis_direction_cls,
        reference_frame_zone_motion_function=reference_frame_zone_motion_function_cls,
    )

