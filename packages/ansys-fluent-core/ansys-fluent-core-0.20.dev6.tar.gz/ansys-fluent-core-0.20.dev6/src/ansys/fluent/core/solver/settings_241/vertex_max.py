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

from .surface_names_2 import surface_names as surface_names_cls
from .geometry_names import geometry_names as geometry_names_cls
from .cust_vec_func import cust_vec_func as cust_vec_func_cls
from .report_of import report_of as report_of_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
class vertex_max(Command):
    """
    Print maximkum of scalar at vertices of the surfaces.
    
    Parameters
    ----------
        surface_names : typing.List[str]
            Select surface.
        geometry_names : typing.List[str]
            Select UTL Geometry.
        cust_vec_func : str
            'cust_vec_func' child.
        report_of : str
            Specify Field.
        current_domain : str
            'current_domain' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
    
    """

    fluent_name = "vertex-max"

    argument_names = \
        ['surface_names', 'geometry_names', 'cust_vec_func', 'report_of',
         'current_domain', 'write_to_file', 'file_name', 'append_data']

    _child_classes = dict(
        surface_names=surface_names_cls,
        geometry_names=geometry_names_cls,
        cust_vec_func=cust_vec_func_cls,
        report_of=report_of_cls,
        current_domain=current_domain_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

