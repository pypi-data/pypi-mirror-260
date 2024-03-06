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

from .filename_6 import filename as filename_cls
from .capacity_1 import capacity as capacity_cls
from .circuit_model import circuit_model as circuit_model_cls
from .fitting_method import fitting_method as fitting_method_cls
from .rs_fix import rs_fix as rs_fix_cls
from .capacity_fade_enabled_1 import capacity_fade_enabled as capacity_fade_enabled_cls
from .read_discharge_file_enabled import read_discharge_file_enabled as read_discharge_file_enabled_cls
from .number_discharge_file import number_discharge_file as number_discharge_file_cls
from .discharge_filename import discharge_filename as discharge_filename_cls
class ecm_curve_fitting(Command):
    """
    ECM parameter estimation tool.
    
    Parameters
    ----------
        filename : typing.List[str]
            File names used in ECM model parameter fitting.
        capacity : real
            Battery capacity used in ECM model parameter fitting.
        circuit_model : str
            Circuit model used in ECM model parameter fitting.
        fitting_method : str
            Fitting method used in ECM model parameter fitting.
        rs_fix : typing.List[real]
            Fix-Rs used in ECM model parameter fitting.
        capacity_fade_enabled : bool
            Include capacity fade effect used in ECM model parameter fitting.
        read_discharge_file_enabled : bool
            Import discharging curves used in ECM model parameter fitting.
        number_discharge_file : int
            Number of total discharging files used in ECM model parameter fitting.
        discharge_filename : typing.List[str]
            File name for discharing curve used in ECM model parameter fitting.
    
    """

    fluent_name = "ecm-curve-fitting"

    argument_names = \
        ['filename', 'capacity', 'circuit_model', 'fitting_method', 'rs_fix',
         'capacity_fade_enabled', 'read_discharge_file_enabled',
         'number_discharge_file', 'discharge_filename']

    _child_classes = dict(
        filename=filename_cls,
        capacity=capacity_cls,
        circuit_model=circuit_model_cls,
        fitting_method=fitting_method_cls,
        rs_fix=rs_fix_cls,
        capacity_fade_enabled=capacity_fade_enabled_cls,
        read_discharge_file_enabled=read_discharge_file_enabled_cls,
        number_discharge_file=number_discharge_file_cls,
        discharge_filename=discharge_filename_cls,
    )

