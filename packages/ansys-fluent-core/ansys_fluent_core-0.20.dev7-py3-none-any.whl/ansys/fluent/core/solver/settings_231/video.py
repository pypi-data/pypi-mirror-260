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

from .background_1 import background as background_cls
from .color_filter import color_filter as color_filter_cls
from .foreground_1 import foreground as foreground_cls
from .on import on as on_cls
from .pixel_size import pixel_size as pixel_size_cls
class video(Group):
    """
    Enter the video window options menu.
    """

    fluent_name = "video"

    child_names = \
        ['background', 'color_filter', 'foreground', 'on', 'pixel_size']

    _child_classes = dict(
        background=background_cls,
        color_filter=color_filter_cls,
        foreground=foreground_cls,
        on=on_cls,
        pixel_size=pixel_size_cls,
    )

