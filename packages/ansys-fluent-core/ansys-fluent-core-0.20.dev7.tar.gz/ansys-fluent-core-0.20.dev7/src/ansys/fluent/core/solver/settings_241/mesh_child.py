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
from .per_zone import per_zone as per_zone_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .cell_zones_3 import cell_zones as cell_zones_cls
from .face_zones import face_zones as face_zones_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class mesh_child(Group):
    """
    'child_object_type' of mesh.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'per_zone', 'average_over',
         'retain_instantaneous_values', 'cell_zones', 'face_zones']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        per_zone=per_zone_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        cell_zones=cell_zones_cls,
        face_zones=face_zones_cls,
        create_output_parameter=create_output_parameter_cls,
    )

