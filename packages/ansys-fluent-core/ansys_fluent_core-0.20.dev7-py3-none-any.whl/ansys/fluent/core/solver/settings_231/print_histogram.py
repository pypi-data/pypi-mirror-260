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

from .domain import domain as domain_cls
from .cell_function import cell_function as cell_function_cls
from .min_val import min_val as min_val_cls
from .max_val import max_val as max_val_cls
from .num_division import num_division as num_division_cls
from .set_all_zones import set_all_zones as set_all_zones_cls
from .threads_list import threads_list as threads_list_cls
from .file_name_1 import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls
class print_histogram(Command):
    """
    Print a histogram of a scalar quantity.
    
    Parameters
    ----------
        domain : str
            'domain' child.
        cell_function : str
            'cell_function' child.
        min_val : real
            'min_val' child.
        max_val : real
            'max_val' child.
        num_division : int
            'num_division' child.
        set_all_zones : bool
            'set_all_zones' child.
        threads_list : typing.List[str]
            'threads_list' child.
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "print-histogram"

    argument_names = \
        ['domain', 'cell_function', 'min_val', 'max_val', 'num_division',
         'set_all_zones', 'threads_list', 'file_name', 'overwrite']

    _child_classes = dict(
        domain=domain_cls,
        cell_function=cell_function_cls,
        min_val=min_val_cls,
        max_val=max_val_cls,
        num_division=num_division_cls,
        set_all_zones=set_all_zones_cls,
        threads_list=threads_list_cls,
        file_name=file_name_cls,
        overwrite=overwrite_cls,
    )

