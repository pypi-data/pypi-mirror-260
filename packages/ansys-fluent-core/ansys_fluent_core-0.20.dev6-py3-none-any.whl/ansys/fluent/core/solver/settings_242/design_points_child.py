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
from .input_parameters import input_parameters as input_parameters_cls
from .output_parameters import output_parameters as output_parameters_cls
from .write_data_2 import write_data as write_data_cls
from .capture_simulation_report_data_1 import capture_simulation_report_data as capture_simulation_report_data_cls
class design_points_child(Group):
    """
    'child_object_type' of design_points.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'input_parameters', 'output_parameters', 'write_data',
         'capture_simulation_report_data']

    _child_classes = dict(
        name=name_cls,
        input_parameters=input_parameters_cls,
        output_parameters=output_parameters_cls,
        write_data=write_data_cls,
        capture_simulation_report_data=capture_simulation_report_data_cls,
    )

