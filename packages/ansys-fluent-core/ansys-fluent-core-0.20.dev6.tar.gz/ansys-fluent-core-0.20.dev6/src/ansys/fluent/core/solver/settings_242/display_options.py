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

from .draw_mesh import draw_mesh as draw_mesh_cls
from .filled import filled as filled_cls
from .marker_1 import marker as marker_cls
from .marker_symbol import marker_symbol as marker_symbol_cls
from .marker_size import marker_size as marker_size_cls
from .wireframe import wireframe as wireframe_cls
from .color_3 import color as color_cls
class display_options(Group):
    """
    'display_options' child.
    """

    fluent_name = "display-options"

    child_names = \
        ['draw_mesh', 'filled', 'marker', 'marker_symbol', 'marker_size',
         'wireframe', 'color']

    _child_classes = dict(
        draw_mesh=draw_mesh_cls,
        filled=filled_cls,
        marker=marker_cls,
        marker_symbol=marker_symbol_cls,
        marker_size=marker_size_cls,
        wireframe=wireframe_cls,
        color=color_cls,
    )

