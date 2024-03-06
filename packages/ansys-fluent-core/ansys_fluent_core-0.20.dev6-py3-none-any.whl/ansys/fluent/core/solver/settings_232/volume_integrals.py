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
from .thread_id_list import thread_id_list as thread_id_list_cls
from .domain import domain as domain_cls
from .cell_function_1 import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls
class volume_integrals(Command):
    """
    Create a volume integral report.
    
    Parameters
    ----------
        report_type : str
            'report_type' child.
        thread_id_list : typing.List[str]
            'thread_id_list' child.
        domain : str
            'domain' child.
        cell_function : str
            'cell_function' child.
        current_domain : str
            'current_domain' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "volume-integrals"

    argument_names = \
        ['report_type', 'thread_id_list', 'domain', 'cell_function',
         'current_domain', 'write_to_file', 'file_name', 'append_data',
         'overwrite']

    _child_classes = dict(
        report_type=report_type_cls,
        thread_id_list=thread_id_list_cls,
        domain=domain_cls,
        cell_function=cell_function_cls,
        current_domain=current_domain_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
        overwrite=overwrite_cls,
    )

