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

from .file_name_1 import file_name as file_name_cls
from .surfaces_2 import surfaces as surfaces_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
class patran_nodal(Command):
    """
    Write a PATRAN nodal results file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surfaces : typing.List[str]
            'surfaces' child.
        cell_func_domain_export : typing.List[str]
            'cell_func_domain_export' child.
    
    """

    fluent_name = "patran-nodal"

    argument_names = \
        ['file_name', 'surfaces', 'cell_func_domain_export']

    _child_classes = dict(
        file_name=file_name_cls,
        surfaces=surfaces_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

