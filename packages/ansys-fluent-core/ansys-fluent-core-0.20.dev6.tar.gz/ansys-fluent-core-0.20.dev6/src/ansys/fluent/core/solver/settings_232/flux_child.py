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

from .name_2 import name as name_cls
from .report_type import report_type as report_type_cls
from .geometry_4 import geometry as geometry_cls
from .physics_1 import physics as physics_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .phase_26 import phase as phase_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .old_props import old_props as old_props_cls
from .zone_names_1 import zone_names as zone_names_cls
from .zone_ids import zone_ids as zone_ids_cls
class flux_child(Group):
    """
    'child_object_type' of flux.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'geometry', 'physics',
         'retain_instantaneous_values', 'phase', 'average_over', 'per_zone',
         'old_props', 'zone_names', 'zone_ids']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        geometry=geometry_cls,
        physics=physics_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        phase=phase_cls,
        average_over=average_over_cls,
        per_zone=per_zone_cls,
        old_props=old_props_cls,
        zone_names=zone_names_cls,
        zone_ids=zone_ids_cls,
    )

