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

from .report_type import report_type as report_type_cls
from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_dens_func import num_dens_func as num_dens_func_cls
from .dia_upper_limit import dia_upper_limit as dia_upper_limit_cls
from .plot_12 import plot as plot_cls
from .print_5 import print as print_cls
from .histogram_2 import histogram as histogram_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
class number_density(Group):
    """
    Number density report.
    """

    fluent_name = "number-density"

    child_names = \
        ['report_type', 'surface_list', 'volume_list', 'num_dens_func',
         'dia_upper_limit']

    command_names = \
        ['plot', 'print', 'histogram', 'write_to_file']

    _child_classes = dict(
        report_type=report_type_cls,
        surface_list=surface_list_cls,
        volume_list=volume_list_cls,
        num_dens_func=num_dens_func_cls,
        dia_upper_limit=dia_upper_limit_cls,
        plot=plot_cls,
        print=print_cls,
        histogram=histogram_cls,
        write_to_file=write_to_file_cls,
    )

