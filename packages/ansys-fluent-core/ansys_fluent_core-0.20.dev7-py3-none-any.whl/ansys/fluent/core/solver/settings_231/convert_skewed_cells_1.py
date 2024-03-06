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

from .cell_thread_list import cell_thread_list as cell_thread_list_cls
from .max_cell_skewness import max_cell_skewness as max_cell_skewness_cls
from .convert_skewed_cells import convert_skewed_cells as convert_skewed_cells_cls
class convert_skewed_cells(Command):
    """
    'convert_skewed_cells' command.
    
    Parameters
    ----------
        cell_thread_list : typing.List[str]
            Set zones where cells should be converted.
        max_cell_skewness : real
            Set target maximum cell skewness.
        convert_skewed_cells : bool
            'convert_skewed_cells' child.
    
    """

    fluent_name = "convert-skewed-cells"

    argument_names = \
        ['cell_thread_list', 'max_cell_skewness', 'convert_skewed_cells']

    _child_classes = dict(
        cell_thread_list=cell_thread_list_cls,
        max_cell_skewness=max_cell_skewness_cls,
        convert_skewed_cells=convert_skewed_cells_cls,
    )

