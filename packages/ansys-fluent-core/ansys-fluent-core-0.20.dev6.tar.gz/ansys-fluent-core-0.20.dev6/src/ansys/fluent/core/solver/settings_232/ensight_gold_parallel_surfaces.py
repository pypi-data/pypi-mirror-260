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

from .name import name as name_cls
from .binary_format import binary_format as binary_format_cls
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls
class ensight_gold_parallel_surfaces(Command):
    """
    Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.
    
    Parameters
    ----------
        name : str
            'name' child.
        binary_format : bool
            'binary_format' child.
        surfaces : typing.List[str]
            'surfaces' child.
        cell_centered : bool
            'cell_centered' child.
        cell_function : typing.List[str]
            'cell_function' child.
    
    """

    fluent_name = "ensight-gold-parallel-surfaces"

    argument_names = \
        ['name', 'binary_format', 'surfaces', 'cell_centered',
         'cell_function']

    _child_classes = dict(
        name=name_cls,
        binary_format=binary_format_cls,
        surfaces=surfaces_cls,
        cell_centered=cell_centered_cls,
        cell_function=cell_function_cls,
    )

