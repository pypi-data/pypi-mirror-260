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
from .structural_analysis import structural_analysis as structural_analysis_cls
from .write_loads import write_loads as write_loads_cls
from .loads import loads as loads_cls
class mechanical_apdl_input(Command):
    """
    Write an Mechanical APDL Input file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surface_name_list : typing.List[str]
            Select surface.
        structural_analysis : bool
            'structural_analysis' child.
        write_loads : bool
            'write_loads' child.
        loads : typing.List[str]
            'loads' child.
    
    """

    fluent_name = "mechanical-apdl-input"

    argument_names = \
        ['file_name', 'surface_name_list', 'structural_analysis',
         'write_loads', 'loads']

    _child_classes = dict(
        file_name=file_name_cls,
        surface_name_list=surface_name_list_cls,
        structural_analysis=structural_analysis_cls,
        write_loads=write_loads_cls,
        loads=loads_cls,
    )

