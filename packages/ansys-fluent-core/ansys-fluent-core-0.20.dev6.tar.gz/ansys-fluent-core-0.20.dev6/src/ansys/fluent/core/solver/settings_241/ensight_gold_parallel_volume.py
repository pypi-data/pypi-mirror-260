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
from .binary_format import binary_format as binary_format_cls
from .cellzones_1 import cellzones as cellzones_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls
class ensight_gold_parallel_volume(Command):
    """
    Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        binary_format : bool
            'binary_format' child.
        cellzones : typing.List[str]
            Enter cell zone name list.
        cell_centered : bool
            'cell_centered' child.
        cell_function : typing.List[str]
            'cell_function' child.
    
    """

    fluent_name = "ensight-gold-parallel-volume"

    argument_names = \
        ['file_name', 'binary_format', 'cellzones', 'cell_centered',
         'cell_function']

    _child_classes = dict(
        file_name=file_name_cls,
        binary_format=binary_format_cls,
        cellzones=cellzones_cls,
        cell_centered=cell_centered_cls,
        cell_function=cell_function_cls,
    )

