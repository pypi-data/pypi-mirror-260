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
from .uid import uid as uid_cls
from .options_12 import options as options_cls
from .filter_settings import filter_settings as filter_settings_cls
from .range import range as range_cls
from .style_attribute_1 import style_attribute as style_attribute_cls
from .vector_settings import vector_settings as vector_settings_cls
from .plot_4 import plot as plot_cls
from .track_single_particle_stream import track_single_particle_stream as track_single_particle_stream_cls
from .skip import skip as skip_cls
from .coarsen_1 import coarsen as coarsen_cls
from .field import field as field_cls
from .injections_list import injections_list as injections_list_cls
from .free_stream_particles import free_stream_particles as free_stream_particles_cls
from .wall_film_particles import wall_film_particles as wall_film_particles_cls
from .track_pdf_particles import track_pdf_particles as track_pdf_particles_cls
from .color_map import color_map as color_map_cls
from .draw_mesh import draw_mesh as draw_mesh_cls
from .mesh_object import mesh_object as mesh_object_cls
from .display_state_name import display_state_name as display_state_name_cls
from .axes_1 import axes as axes_cls
from .curves_1 import curves as curves_cls
from .display_3 import display as display_cls
from .update_min_max import update_min_max as update_min_max_cls
class particle_track_child(Group):
    """
    'child_object_type' of particle_track.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'filter_settings', 'range',
         'style_attribute', 'vector_settings', 'plot',
         'track_single_particle_stream', 'skip', 'coarsen', 'field',
         'injections_list', 'free_stream_particles', 'wall_film_particles',
         'track_pdf_particles', 'color_map', 'draw_mesh', 'mesh_object',
         'display_state_name', 'axes', 'curves']

    command_names = \
        ['display', 'update_min_max']

    _child_classes = dict(
        name=name_cls,
        uid=uid_cls,
        options=options_cls,
        filter_settings=filter_settings_cls,
        range=range_cls,
        style_attribute=style_attribute_cls,
        vector_settings=vector_settings_cls,
        plot=plot_cls,
        track_single_particle_stream=track_single_particle_stream_cls,
        skip=skip_cls,
        coarsen=coarsen_cls,
        field=field_cls,
        injections_list=injections_list_cls,
        free_stream_particles=free_stream_particles_cls,
        wall_film_particles=wall_film_particles_cls,
        track_pdf_particles=track_pdf_particles_cls,
        color_map=color_map_cls,
        draw_mesh=draw_mesh_cls,
        mesh_object=mesh_object_cls,
        display_state_name=display_state_name_cls,
        axes=axes_cls,
        curves=curves_cls,
        display=display_cls,
        update_min_max=update_min_max_cls,
    )

