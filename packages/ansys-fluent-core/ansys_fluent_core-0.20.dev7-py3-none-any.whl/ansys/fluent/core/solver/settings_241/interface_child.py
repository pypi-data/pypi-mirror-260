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
from .phase_7 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .non_overlap_zone_name import non_overlap_zone_name as non_overlap_zone_name_cls
class interface_child(Group):
    """
    'child_object_type' of interface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x',
         'geom_dir_y', 'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'non_overlap_zone_name']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        geom_disable=geom_disable_cls,
        geom_dir_spec=geom_dir_spec_cls,
        geom_dir_x=geom_dir_x_cls,
        geom_dir_y=geom_dir_y_cls,
        geom_dir_z=geom_dir_z_cls,
        geom_levels=geom_levels_cls,
        geom_bgthread=geom_bgthread_cls,
        non_overlap_zone_name=non_overlap_zone_name_cls,
    )

