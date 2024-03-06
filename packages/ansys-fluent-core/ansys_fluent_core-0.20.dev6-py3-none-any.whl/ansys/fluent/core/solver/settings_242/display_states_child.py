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
from .front_faces_transparent import front_faces_transparent as front_faces_transparent_cls
from .projection_1 import projection as projection_cls
from .axes_2 import axes as axes_cls
from .ruler import ruler as ruler_cls
from .title import title as title_cls
from .boundary_marker import boundary_marker as boundary_marker_cls
from .anti_aliasing import anti_aliasing as anti_aliasing_cls
from .reflections import reflections as reflections_cls
from .static_shadows import static_shadows as static_shadows_cls
from .dynamic_shadows import dynamic_shadows as dynamic_shadows_cls
from .grid_plane import grid_plane as grid_plane_cls
from .headlights import headlights as headlights_cls
from .lighting_1 import lighting as lighting_cls
from .view_name import view_name as view_name_cls
class display_states_child(Group):
    """
    'child_object_type' of display_states.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'front_faces_transparent', 'projection', 'axes', 'ruler',
         'title', 'boundary_marker', 'anti_aliasing', 'reflections',
         'static_shadows', 'dynamic_shadows', 'grid_plane', 'headlights',
         'lighting', 'view_name']

    _child_classes = dict(
        name=name_cls,
        front_faces_transparent=front_faces_transparent_cls,
        projection=projection_cls,
        axes=axes_cls,
        ruler=ruler_cls,
        title=title_cls,
        boundary_marker=boundary_marker_cls,
        anti_aliasing=anti_aliasing_cls,
        reflections=reflections_cls,
        static_shadows=static_shadows_cls,
        dynamic_shadows=dynamic_shadows_cls,
        grid_plane=grid_plane_cls,
        headlights=headlights_cls,
        lighting=lighting_cls,
        view_name=view_name_cls,
    )

