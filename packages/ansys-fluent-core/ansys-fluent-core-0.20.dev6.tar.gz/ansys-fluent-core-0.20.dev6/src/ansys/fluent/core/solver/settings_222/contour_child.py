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

from .name import name as name_cls
from .field import field as field_cls
from .filled import filled as filled_cls
from .boundary_values import boundary_values as boundary_values_cls
from .contour_lines import contour_lines as contour_lines_cls
from .node_values import node_values as node_values_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .range_option import range_option as range_option_cls
from .coloring_1 import coloring as coloring_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_1 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .display_1 import display as display_cls
class contour_child(Group):
    """
    'child_object_type' of contour.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'filled', 'boundary_values', 'contour_lines',
         'node_values', 'surfaces_list', 'range_option', 'coloring',
         'color_map', 'draw_mesh', 'mesh_object', 'display_state_name',
         'physics', 'geometry', 'surfaces']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        field=field_cls,
        filled=filled_cls,
        boundary_values=boundary_values_cls,
        contour_lines=contour_lines_cls,
        node_values=node_values_cls,
        surfaces_list=surfaces_list_cls,
        range_option=range_option_cls,
        coloring=coloring_cls,
        color_map=color_map_cls,
        draw_mesh=draw_mesh_cls,
        mesh_object=mesh_object_cls,
        display_state_name=display_state_name_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        surfaces=surfaces_cls,
        display=display_cls,
    )

