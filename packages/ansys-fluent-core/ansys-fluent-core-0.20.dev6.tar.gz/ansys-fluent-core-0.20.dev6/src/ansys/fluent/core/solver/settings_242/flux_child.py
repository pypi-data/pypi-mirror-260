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
from .boundaries_1 import boundaries as boundaries_cls
from .per_zone import per_zone as per_zone_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .phase_31 import phase as phase_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class flux_child(Group):
    """
    'child_object_type' of flux.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'boundaries', 'per_zone', 'average_over',
         'retain_instantaneous_values', 'phase', 'physics', 'geometry']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        boundaries=boundaries_cls,
        per_zone=per_zone_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        phase=phase_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        create_output_parameter=create_output_parameter_cls,
    )

