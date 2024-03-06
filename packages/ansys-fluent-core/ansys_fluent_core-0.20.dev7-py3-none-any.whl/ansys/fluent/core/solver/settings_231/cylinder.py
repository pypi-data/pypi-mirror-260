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

from .axis_begin import axis_begin as axis_begin_cls
from .axis_end import axis_end as axis_end_cls
from .radius import radius as radius_cls
from .inside import inside as inside_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls
class cylinder(Group):
    """
    'cylinder' child.
    """

    fluent_name = "cylinder"

    child_names = \
        ['axis_begin', 'axis_end', 'radius', 'inside',
         'create_volume_surface']

    _child_classes = dict(
        axis_begin=axis_begin_cls,
        axis_end=axis_end_cls,
        radius=radius_cls,
        inside=inside_cls,
        create_volume_surface=create_volume_surface_cls,
    )

