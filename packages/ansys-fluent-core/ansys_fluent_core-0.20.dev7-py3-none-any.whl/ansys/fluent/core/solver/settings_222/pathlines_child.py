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
from .uid import uid as uid_cls
from .options_5 import options as options_cls
from .range import range as range_cls
from .style_attribute import style_attribute as style_attribute_cls
from .accuracy_control import accuracy_control as accuracy_control_cls
from .plot import plot as plot_cls
from .step import step as step_cls
from .skip import skip as skip_cls
from .coarsen import coarsen as coarsen_cls
from .onzone import onzone as onzone_cls
from .field import field as field_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .velocity_domain import velocity_domain as velocity_domain_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_1 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .display_1 import display as display_cls
class pathlines_child(Group):
    """
    'child_object_type' of pathlines.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'range', 'style_attribute',
         'accuracy_control', 'plot', 'step', 'skip', 'coarsen', 'onzone',
         'field', 'surfaces_list', 'velocity_domain', 'color_map',
         'draw_mesh', 'mesh_object', 'display_state_name', 'physics',
         'geometry', 'surfaces']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        uid=uid_cls,
        options=options_cls,
        range=range_cls,
        style_attribute=style_attribute_cls,
        accuracy_control=accuracy_control_cls,
        plot=plot_cls,
        step=step_cls,
        skip=skip_cls,
        coarsen=coarsen_cls,
        onzone=onzone_cls,
        field=field_cls,
        surfaces_list=surfaces_list_cls,
        velocity_domain=velocity_domain_cls,
        color_map=color_map_cls,
        draw_mesh=draw_mesh_cls,
        mesh_object=mesh_object_cls,
        display_state_name=display_state_name_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        surfaces=surfaces_cls,
        display=display_cls,
    )

