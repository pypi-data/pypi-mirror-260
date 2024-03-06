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
from .field import field as field_cls
from .surface_names import surface_names as surface_names_cls
from .per_surface import per_surface as per_surface_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .custom_vector import custom_vector as custom_vector_cls
from .phase_31 import phase as phase_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .surfaces_4 import surfaces as surfaces_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class surface_child(Group):
    """
    'child_object_type' of surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'field', 'surface_names', 'per_surface',
         'average_over', 'retain_instantaneous_values', 'custom_vector',
         'phase', 'physics', 'geometry', 'surfaces']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        field=field_cls,
        surface_names=surface_names_cls,
        per_surface=per_surface_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        custom_vector=custom_vector_cls,
        phase=phase_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        surfaces=surfaces_cls,
        create_output_parameter=create_output_parameter_cls,
    )

