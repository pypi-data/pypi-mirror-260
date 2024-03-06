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

from .min_point import min_point as min_point_cls
from .max_point import max_point as max_point_cls
from .inside import inside as inside_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls
class hexahedron(Group):
    """
    'hexahedron' child.
    """

    fluent_name = "hexahedron"

    child_names = \
        ['min_point', 'max_point', 'inside', 'create_volume_surface']

    _child_classes = dict(
        min_point=min_point_cls,
        max_point=max_point_cls,
        inside=inside_cls,
        create_volume_surface=create_volume_surface_cls,
    )

