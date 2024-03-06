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

from .point_surface import point_surface as point_surface_cls
from .line_surface import line_surface as line_surface_cls
from .rake_surface import rake_surface as rake_surface_cls
from .plane_surface import plane_surface as plane_surface_cls
from .iso_surface import iso_surface as iso_surface_cls
from .iso_clip import iso_clip as iso_clip_cls
from .zone_surface import zone_surface as zone_surface_cls
from .partition_surface import partition_surface as partition_surface_cls
from .transform_surface import transform_surface as transform_surface_cls
from .imprint_surface import imprint_surface as imprint_surface_cls
from .plane_slice import plane_slice as plane_slice_cls
from .sphere_slice import sphere_slice as sphere_slice_cls
from .quadric_surface import quadric_surface as quadric_surface_cls
from .surface_cells import surface_cells as surface_cells_cls
from .create_multiple_zone_surfaces import create_multiple_zone_surfaces as create_multiple_zone_surfaces_cls
from .create_multiple_iso_surfaces import create_multiple_iso_surfaces as create_multiple_iso_surfaces_cls
from .create_group_surfaces import create_group_surfaces as create_group_surfaces_cls
from .ungroup_surfaces import ungroup_surfaces as ungroup_surfaces_cls
from .set_rendering_priority import set_rendering_priority as set_rendering_priority_cls
from .reset_zone_surfaces import reset_zone_surfaces as reset_zone_surfaces_cls
class surfaces(Group):
    """
    'surfaces' child.
    """

    fluent_name = "surfaces"

    child_names = \
        ['point_surface', 'line_surface', 'rake_surface', 'plane_surface',
         'iso_surface', 'iso_clip', 'zone_surface', 'partition_surface',
         'transform_surface', 'imprint_surface', 'plane_slice',
         'sphere_slice', 'quadric_surface', 'surface_cells']

    command_names = \
        ['create_multiple_zone_surfaces', 'create_multiple_iso_surfaces',
         'create_group_surfaces', 'ungroup_surfaces',
         'set_rendering_priority', 'reset_zone_surfaces']

    _child_classes = dict(
        point_surface=point_surface_cls,
        line_surface=line_surface_cls,
        rake_surface=rake_surface_cls,
        plane_surface=plane_surface_cls,
        iso_surface=iso_surface_cls,
        iso_clip=iso_clip_cls,
        zone_surface=zone_surface_cls,
        partition_surface=partition_surface_cls,
        transform_surface=transform_surface_cls,
        imprint_surface=imprint_surface_cls,
        plane_slice=plane_slice_cls,
        sphere_slice=sphere_slice_cls,
        quadric_surface=quadric_surface_cls,
        surface_cells=surface_cells_cls,
        create_multiple_zone_surfaces=create_multiple_zone_surfaces_cls,
        create_multiple_iso_surfaces=create_multiple_iso_surfaces_cls,
        create_group_surfaces=create_group_surfaces_cls,
        ungroup_surfaces=ungroup_surfaces_cls,
        set_rendering_priority=set_rendering_priority_cls,
        reset_zone_surfaces=reset_zone_surfaces_cls,
    )

