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

from .enable_high_res_tracking import enable_high_res_tracking as enable_high_res_tracking_cls
from .expert_options_1 import expert_options as expert_options_cls
from .high_res_tracking_options import high_res_tracking_options as high_res_tracking_options_cls
from .tracking_parameters import tracking_parameters as tracking_parameters_cls
from .track_in_absolute_frame import track_in_absolute_frame as track_in_absolute_frame_cls
class tracking(Group):
    """
    Main menu to control the time integration of the particle trajectory equations.
    """

    fluent_name = "tracking"

    child_names = \
        ['enable_high_res_tracking', 'expert_options',
         'high_res_tracking_options', 'tracking_parameters',
         'track_in_absolute_frame']

    _child_classes = dict(
        enable_high_res_tracking=enable_high_res_tracking_cls,
        expert_options=expert_options_cls,
        high_res_tracking_options=high_res_tracking_options_cls,
        tracking_parameters=tracking_parameters_cls,
        track_in_absolute_frame=track_in_absolute_frame_cls,
    )

