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
from .method_11 import method as method_cls
from .x_3 import x as x_cls
from .y_3 import y as y_cls
from .z_1 import z as z_cls
from .point_1 import point as point_cls
from .normal_computation_method import normal_computation_method as normal_computation_method_cls
from .surface_aligned_normal import surface_aligned_normal as surface_aligned_normal_cls
from .normal import normal as normal_cls
from .p0_1 import p0 as p0_cls
from .p1_1 import p1 as p1_cls
from .p2 import p2 as p2_cls
from .bounded import bounded as bounded_cls
from .sample_points import sample_points as sample_points_cls
from .edges import edges as edges_cls
from .display_4 import display as display_cls
class plane_surface_child(Group):
    """
    'child_object_type' of plane_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'method', 'x', 'y', 'z', 'point',
         'normal_computation_method', 'surface_aligned_normal', 'normal',
         'p0', 'p1', 'p2', 'bounded', 'sample_points', 'edges']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        method=method_cls,
        x=x_cls,
        y=y_cls,
        z=z_cls,
        point=point_cls,
        normal_computation_method=normal_computation_method_cls,
        surface_aligned_normal=surface_aligned_normal_cls,
        normal=normal_cls,
        p0=p0_cls,
        p1=p1_cls,
        p2=p2_cls,
        bounded=bounded_cls,
        sample_points=sample_points_cls,
        edges=edges_cls,
        display=display_cls,
    )

    _child_aliases = dict(
        point_normal="normal",
        point_vector="point",
    )

