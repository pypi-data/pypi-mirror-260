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

from .mesh_2 import mesh as mesh_cls
from .contour import contour as contour_cls
from .vector_1 import vector as vector_cls
from .pathline import pathline as pathline_cls
from .particle_track import particle_track as particle_track_cls
from .lic import lic as lic_cls
from .olic import olic as olic_cls
from .volumes_1 import volumes as volumes_cls
from .contours import contours as contours_cls
from .particle_tracks import particle_tracks as particle_tracks_cls
from .colors import colors as colors_cls
from .lighting import lighting as lighting_cls
from .picture import picture as picture_cls
from .views import views as views_cls
from .windows import windows as windows_cls
from .raytracing_options import raytracing_options as raytracing_options_cls
from .pulse import pulse as pulse_cls
class graphics(Group, _ChildNamedObjectAccessorMixin):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['mesh', 'contour', 'vector', 'pathline', 'particle_track', 'lic',
         'olic', 'volumes', 'contours', 'particle_tracks', 'colors',
         'lighting', 'picture', 'views', 'windows', 'raytracing_options',
         'pulse']

    _child_classes = dict(
        mesh=mesh_cls,
        contour=contour_cls,
        vector=vector_cls,
        pathline=pathline_cls,
        particle_track=particle_track_cls,
        lic=lic_cls,
        olic=olic_cls,
        volumes=volumes_cls,
        contours=contours_cls,
        particle_tracks=particle_tracks_cls,
        colors=colors_cls,
        lighting=lighting_cls,
        picture=picture_cls,
        views=views_cls,
        windows=windows_cls,
        raytracing_options=raytracing_options_cls,
        pulse=pulse_cls,
    )

