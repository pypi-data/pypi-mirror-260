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
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
class gambit(Command):
    """
    Write a Gambit neutral file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        cell_func_domain_export : typing.List[str]
            'cell_func_domain_export' child.
    
    """

    fluent_name = "gambit"

    argument_names = \
        ['file_name', 'cell_func_domain_export']

    _child_classes = dict(
        file_name=file_name_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

