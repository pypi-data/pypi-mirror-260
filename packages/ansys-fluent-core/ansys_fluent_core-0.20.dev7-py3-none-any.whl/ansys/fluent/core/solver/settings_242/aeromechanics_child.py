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
from .zones_2 import zones as zones_cls
from .per_zone import per_zone as per_zone_cls
from .nodal_diameters import nodal_diameters as nodal_diameters_cls
from .average_over import average_over as average_over_cls
from .integrate_over import integrate_over as integrate_over_cls
from .normalization import normalization as normalization_cls
from .realcomponent import realcomponent as realcomponent_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class aeromechanics_child(Group):
    """
    'child_object_type' of aeromechanics.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'zones', 'per_zone', 'nodal_diameters',
         'average_over', 'integrate_over', 'normalization', 'realcomponent']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        zones=zones_cls,
        per_zone=per_zone_cls,
        nodal_diameters=nodal_diameters_cls,
        average_over=average_over_cls,
        integrate_over=integrate_over_cls,
        normalization=normalization_cls,
        realcomponent=realcomponent_cls,
        create_output_parameter=create_output_parameter_cls,
    )

