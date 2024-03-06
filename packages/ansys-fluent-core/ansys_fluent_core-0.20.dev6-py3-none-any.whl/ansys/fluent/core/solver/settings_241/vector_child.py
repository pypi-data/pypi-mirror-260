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
from .field import field as field_cls
from .vector_field import vector_field as vector_field_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .scale_3 import scale as scale_cls
from .style import style as style_cls
from .skip import skip as skip_cls
from .vector_opt import vector_opt as vector_opt_cls
from .range_option import range_option as range_option_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics_1 import physics as physics_cls
from .geometry_5 import geometry as geometry_cls
from .surfaces_4 import surfaces as surfaces_cls
from .display_3 import display as display_cls
from .update_min_max import update_min_max as update_min_max_cls
class vector_child(Group):
    """
    'child_object_type' of vector.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'vector_field', 'surfaces_list', 'scale', 'style',
         'skip', 'vector_opt', 'range_option', 'color_map', 'draw_mesh',
         'mesh_object', 'display_state_name', 'physics', 'geometry',
         'surfaces']

    command_names = \
        ['display', 'update_min_max']

    _child_classes = dict(
        name=name_cls,
        field=field_cls,
        vector_field=vector_field_cls,
        surfaces_list=surfaces_list_cls,
        scale=scale_cls,
        style=style_cls,
        skip=skip_cls,
        vector_opt=vector_opt_cls,
        range_option=range_option_cls,
        color_map=color_map_cls,
        draw_mesh=draw_mesh_cls,
        mesh_object=mesh_object_cls,
        display_state_name=display_state_name_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        surfaces=surfaces_cls,
        display=display_cls,
        update_min_max=update_min_max_cls,
    )

