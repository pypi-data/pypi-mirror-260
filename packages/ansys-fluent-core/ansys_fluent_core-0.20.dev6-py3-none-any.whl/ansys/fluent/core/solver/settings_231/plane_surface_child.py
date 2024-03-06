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

from .methods_2 import methods as methods_cls
from .x import x as x_cls
from .y import y as y_cls
from .z import z as z_cls
from .point_vector import point_vector as point_vector_cls
from .point_normal import point_normal as point_normal_cls
from .compute_from_view_plane import compute_from_view_plane as compute_from_view_plane_cls
from .surface_aligned_normal import surface_aligned_normal as surface_aligned_normal_cls
from .p0 import p0 as p0_cls
from .p1 import p1 as p1_cls
from .p2 import p2 as p2_cls
from .bounded import bounded as bounded_cls
from .sample_point import sample_point as sample_point_cls
from .edges_2 import edges as edges_cls
class plane_surface_child(Group):
    """
    'child_object_type' of plane_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['methods', 'x', 'y', 'z', 'point_vector', 'point_normal',
         'compute_from_view_plane', 'surface_aligned_normal', 'p0', 'p1',
         'p2', 'bounded', 'sample_point', 'edges']

    _child_classes = dict(
        methods=methods_cls,
        x=x_cls,
        y=y_cls,
        z=z_cls,
        point_vector=point_vector_cls,
        point_normal=point_normal_cls,
        compute_from_view_plane=compute_from_view_plane_cls,
        surface_aligned_normal=surface_aligned_normal_cls,
        p0=p0_cls,
        p1=p1_cls,
        p2=p2_cls,
        bounded=bounded_cls,
        sample_point=sample_point_cls,
        edges=edges_cls,
    )

