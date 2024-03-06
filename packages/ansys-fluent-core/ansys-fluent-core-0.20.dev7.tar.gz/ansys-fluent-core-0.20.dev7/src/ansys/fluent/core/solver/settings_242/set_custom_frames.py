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

from .start_frame import start_frame as start_frame_cls
from .end_frame import end_frame as end_frame_cls
from .increment import increment as increment_cls
class set_custom_frames(Group):
    """
    Set custom frames start, end, skip frames for video export.
    """

    fluent_name = "set-custom-frames"

    child_names = \
        ['start_frame', 'end_frame', 'increment']

    _child_classes = dict(
        start_frame=start_frame_cls,
        end_frame=end_frame_cls,
        increment=increment_cls,
    )

