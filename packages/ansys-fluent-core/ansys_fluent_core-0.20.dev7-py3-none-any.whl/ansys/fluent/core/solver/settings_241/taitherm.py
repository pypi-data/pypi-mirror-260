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
from .surface_name_list import surface_name_list as surface_name_list_cls
from .wall_function import wall_function as wall_function_cls
from .htc_on_walls import htc_on_walls as htc_on_walls_cls
class taitherm(Command):
    """
    Write a TAITherm file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surface_name_list : typing.List[str]
            Select surface.
        wall_function : bool
            'wall_function' child.
        htc_on_walls : bool
            'htc_on_walls' child.
    
    """

    fluent_name = "taitherm"

    argument_names = \
        ['file_name', 'surface_name_list', 'wall_function', 'htc_on_walls']

    _child_classes = dict(
        file_name=file_name_cls,
        surface_name_list=surface_name_list_cls,
        wall_function=wall_function_cls,
        htc_on_walls=htc_on_walls_cls,
    )

