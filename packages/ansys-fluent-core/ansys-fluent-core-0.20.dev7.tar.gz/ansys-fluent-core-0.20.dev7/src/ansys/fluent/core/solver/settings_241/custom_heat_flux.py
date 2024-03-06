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
from .wall_function import wall_function as wall_function_cls
from .surface_name_list import surface_name_list as surface_name_list_cls
class custom_heat_flux(Command):
    """
    Write a generic file for heat transfer.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        wall_function : bool
            'wall_function' child.
        surface_name_list : typing.List[str]
            Select surface.
    
    """

    fluent_name = "custom-heat-flux"

    argument_names = \
        ['file_name', 'wall_function', 'surface_name_list']

    _child_classes = dict(
        file_name=file_name_cls,
        wall_function=wall_function_cls,
        surface_name_list=surface_name_list_cls,
    )

