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
from .surface_name_list import surface_name_list as surface_name_list_cls
from .structural_analysis import structural_analysis as structural_analysis_cls
from .write_loads import write_loads as write_loads_cls
from .loads import loads as loads_cls
class abaqus(Command):
    """
    Write an ABAQUS file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surface_name_list : typing.List[str]
            'surface_name_list' child.
        structural_analysis : bool
            'structural_analysis' child.
        write_loads : bool
            'write_loads' child.
        loads : typing.List[str]
            'loads' child.
    
    """

    fluent_name = "abaqus"

    argument_names = \
        ['name', 'surface_name_list', 'structural_analysis', 'write_loads',
         'loads']

    _child_classes = dict(
        name=name_cls,
        surface_name_list=surface_name_list_cls,
        structural_analysis=structural_analysis_cls,
        write_loads=write_loads_cls,
        loads=loads_cls,
    )

