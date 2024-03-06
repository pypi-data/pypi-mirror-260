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

from .mesh_1 import mesh as mesh_cls
from .contour import contour as contour_cls
from .vector import vector as vector_cls
from .pathlines import pathlines as pathlines_cls
from .particle_tracks import particle_tracks as particle_tracks_cls
from .lic import lic as lic_cls
from .views import views as views_cls
class graphics(Group):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['mesh', 'contour', 'vector', 'pathlines', 'particle_tracks', 'lic',
         'views']

    _child_classes = dict(
        mesh=mesh_cls,
        contour=contour_cls,
        vector=vector_cls,
        pathlines=pathlines_cls,
        particle_tracks=particle_tracks_cls,
        lic=lic_cls,
        views=views_cls,
    )

