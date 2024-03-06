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
from .surfaces_1 import surfaces as surfaces_cls
from .cellzones import cellzones as cellzones_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls
class fieldview_unstruct_data(Command):
    """
    Write a Fieldview unstructured results only file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surfaces : typing.List[str]
            List of surfaces to export.
        cellzones : typing.List[str]
            List of cell zones to export.
        cell_func_domain : typing.List[str]
            'cell_func_domain' child.
    
    """

    fluent_name = "fieldview-unstruct-data"

    argument_names = \
        ['file_name', 'surfaces', 'cellzones', 'cell_func_domain']

    _child_classes = dict(
        file_name=file_name_cls,
        surfaces=surfaces_cls,
        cellzones=cellzones_cls,
        cell_func_domain=cell_func_domain_cls,
    )

