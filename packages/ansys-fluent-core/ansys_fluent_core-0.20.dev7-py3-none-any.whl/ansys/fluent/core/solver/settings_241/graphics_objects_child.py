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

from .name_1 import name as name_cls
from .transparency_1 import transparency as transparency_cls
from .colormap_position import colormap_position as colormap_position_cls
from .colormap_left import colormap_left as colormap_left_cls
from .colormap_bottom import colormap_bottom as colormap_bottom_cls
from .colormap_width import colormap_width as colormap_width_cls
from .colormap_height import colormap_height as colormap_height_cls
class graphics_objects_child(Group):
    """
    'child_object_type' of graphics_objects.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'transparency', 'colormap_position', 'colormap_left',
         'colormap_bottom', 'colormap_width', 'colormap_height']

    _child_classes = dict(
        name=name_cls,
        transparency=transparency_cls,
        colormap_position=colormap_position_cls,
        colormap_left=colormap_left_cls,
        colormap_bottom=colormap_bottom_cls,
        colormap_width=colormap_width_cls,
        colormap_height=colormap_height_cls,
    )

