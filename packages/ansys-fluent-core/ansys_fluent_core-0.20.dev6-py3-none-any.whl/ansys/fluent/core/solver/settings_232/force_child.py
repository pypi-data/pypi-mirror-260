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
from .scaled import scaled as scaled_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .thread_names import thread_names as thread_names_cls
from .thread_ids import thread_ids as thread_ids_cls
from .old_props import old_props as old_props_cls
from .reference_frame import reference_frame as reference_frame_cls
from .force_vector import force_vector as force_vector_cls
class force_child(Group):
    """
    'child_object_type' of force.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'geometry', 'physics',
         'retain_instantaneous_values', 'scaled', 'average_over', 'per_zone',
         'thread_names', 'thread_ids', 'old_props', 'reference_frame',
         'force_vector']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        geometry=geometry_cls,
        physics=physics_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        scaled=scaled_cls,
        average_over=average_over_cls,
        per_zone=per_zone_cls,
        thread_names=thread_names_cls,
        thread_ids=thread_ids_cls,
        old_props=old_props_cls,
        reference_frame=reference_frame_cls,
        force_vector=force_vector_cls,
    )

