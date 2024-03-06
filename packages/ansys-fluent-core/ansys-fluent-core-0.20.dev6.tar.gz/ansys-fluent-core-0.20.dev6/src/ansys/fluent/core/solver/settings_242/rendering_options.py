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

from .animation_option import animation_option as animation_option_cls
from .auto_spin import auto_spin as auto_spin_cls
from .color_map_alignment import color_map_alignment as color_map_alignment_cls
from .double_buffering import double_buffering as double_buffering_cls
from .face_displacement import face_displacement as face_displacement_cls
from .hidden_surface_method import hidden_surface_method as hidden_surface_method_cls
from .hidden_surfaces import hidden_surfaces as hidden_surfaces_cls
from .front_faces_transparent_1 import front_faces_transparent as front_faces_transparent_cls
from .show_colormap import show_colormap as show_colormap_cls
from .device_info import device_info as device_info_cls
from .driver import driver as driver_cls
from .set_rendering_options import set_rendering_options as set_rendering_options_cls
class rendering_options(Group):
    """
    'rendering_options' child.
    """

    fluent_name = "rendering-options"

    child_names = \
        ['animation_option', 'auto_spin', 'color_map_alignment',
         'double_buffering', 'face_displacement', 'hidden_surface_method',
         'hidden_surfaces', 'front_faces_transparent', 'show_colormap']

    command_names = \
        ['device_info', 'driver', 'set_rendering_options']

    _child_classes = dict(
        animation_option=animation_option_cls,
        auto_spin=auto_spin_cls,
        color_map_alignment=color_map_alignment_cls,
        double_buffering=double_buffering_cls,
        face_displacement=face_displacement_cls,
        hidden_surface_method=hidden_surface_method_cls,
        hidden_surfaces=hidden_surfaces_cls,
        front_faces_transparent=front_faces_transparent_cls,
        show_colormap=show_colormap_cls,
        device_info=device_info_cls,
        driver=driver_cls,
        set_rendering_options=set_rendering_options_cls,
    )

