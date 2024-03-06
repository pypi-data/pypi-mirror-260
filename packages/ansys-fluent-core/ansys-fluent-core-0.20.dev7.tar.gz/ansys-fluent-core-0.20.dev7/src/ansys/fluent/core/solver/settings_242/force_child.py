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
from .report_type import report_type as report_type_cls
from .force_vector import force_vector as force_vector_cls
from .reference_frame import reference_frame as reference_frame_cls
from .zones_2 import zones as zones_cls
from .per_zone import per_zone as per_zone_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .report_output_type import report_output_type as report_output_type_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class force_child(Group):
    """
    'child_object_type' of force.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'force_vector', 'reference_frame', 'zones',
         'per_zone', 'average_over', 'retain_instantaneous_values',
         'report_output_type', 'physics', 'geometry']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        force_vector=force_vector_cls,
        reference_frame=reference_frame_cls,
        zones=zones_cls,
        per_zone=per_zone_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        report_output_type=report_output_type_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        create_output_parameter=create_output_parameter_cls,
    )

