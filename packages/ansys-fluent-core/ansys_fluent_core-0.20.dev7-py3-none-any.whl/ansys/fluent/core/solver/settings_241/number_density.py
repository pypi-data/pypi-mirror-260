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
from .disc_output_type import disc_output_type as disc_output_type_cls
from .qmom_output_type import qmom_output_type as qmom_output_type_cls
from .smm_output_type import smm_output_type as smm_output_type_cls
from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_dens_func import num_dens_func as num_dens_func_cls
from .dia_upper_limit import dia_upper_limit as dia_upper_limit_cls
from .file_name_1 import file_name as file_name_cls
class number_density(Command):
    """
    'number_density' command.
    
    Parameters
    ----------
        report_type : str
            'report_type' child.
        disc_output_type : str
            'disc_output_type' child.
        qmom_output_type : str
            'qmom_output_type' child.
        smm_output_type : str
            'smm_output_type' child.
        surface_list : typing.List[str]
            Select surface.
        volume_list : typing.List[str]
            Enter cell zone name list.
        num_dens_func : str
            'num_dens_func' child.
        dia_upper_limit : real
            'dia_upper_limit' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "number-density"

    argument_names = \
        ['report_type', 'disc_output_type', 'qmom_output_type',
         'smm_output_type', 'surface_list', 'volume_list', 'num_dens_func',
         'dia_upper_limit', 'file_name']

    _child_classes = dict(
        report_type=report_type_cls,
        disc_output_type=disc_output_type_cls,
        qmom_output_type=qmom_output_type_cls,
        smm_output_type=smm_output_type_cls,
        surface_list=surface_list_cls,
        volume_list=volume_list_cls,
        num_dens_func=num_dens_func_cls,
        dia_upper_limit=dia_upper_limit_cls,
        file_name=file_name_cls,
    )

