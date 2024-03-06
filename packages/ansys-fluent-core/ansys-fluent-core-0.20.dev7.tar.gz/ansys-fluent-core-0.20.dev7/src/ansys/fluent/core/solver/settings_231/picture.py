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

from .color_mode import color_mode as color_mode_cls
from .driver_options import driver_options as driver_options_cls
from .invert_background import invert_background as invert_background_cls
from .landscape import landscape as landscape_cls
from .x_resolution import x_resolution as x_resolution_cls
from .y_resolution import y_resolution as y_resolution_cls
from .dpi import dpi as dpi_cls
from .use_window_resolution import use_window_resolution as use_window_resolution_cls
from .standard_resolution import standard_resolution as standard_resolution_cls
from .jpeg_hardcopy_quality import jpeg_hardcopy_quality as jpeg_hardcopy_quality_cls
from .preview import preview as preview_cls
from .save_picture import save_picture as save_picture_cls
from .list_color_mode import list_color_mode as list_color_mode_cls
class picture(Group):
    """
    Enter the hardcopy/save-picture options menu.
    """

    fluent_name = "picture"

    child_names = \
        ['color_mode', 'driver_options', 'invert_background', 'landscape',
         'x_resolution', 'y_resolution', 'dpi', 'use_window_resolution',
         'standard_resolution', 'jpeg_hardcopy_quality']

    command_names = \
        ['preview', 'save_picture', 'list_color_mode']

    _child_classes = dict(
        color_mode=color_mode_cls,
        driver_options=driver_options_cls,
        invert_background=invert_background_cls,
        landscape=landscape_cls,
        x_resolution=x_resolution_cls,
        y_resolution=y_resolution_cls,
        dpi=dpi_cls,
        use_window_resolution=use_window_resolution_cls,
        standard_resolution=standard_resolution_cls,
        jpeg_hardcopy_quality=jpeg_hardcopy_quality_cls,
        preview=preview_cls,
        save_picture=save_picture_cls,
        list_color_mode=list_color_mode_cls,
    )

