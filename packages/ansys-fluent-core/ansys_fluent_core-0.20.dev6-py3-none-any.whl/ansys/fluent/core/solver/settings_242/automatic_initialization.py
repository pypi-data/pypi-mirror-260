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

from .initialization_type_1 import initialization_type as initialization_type_cls
from .data_file_name import data_file_name as data_file_name_cls
from .init_from_solution_1 import init_from_solution as init_from_solution_cls
from .data_file_name2 import data_file_name2 as data_file_name2_cls
class automatic_initialization(Command):
    """
    Define how the case is to be initialized automatically.
    
    Parameters
    ----------
        initialization_type : str
            'initialization_type' child.
        data_file_name : str
            'data_file_name' child.
        init_from_solution : str
            'init_from_solution' child.
        data_file_name2 : str
            'data_file_name2' child.
    
    """

    fluent_name = "automatic-initialization"

    argument_names = \
        ['initialization_type', 'data_file_name', 'init_from_solution',
         'data_file_name2']

    _child_classes = dict(
        initialization_type=initialization_type_cls,
        data_file_name=data_file_name_cls,
        init_from_solution=init_from_solution_cls,
        data_file_name2=data_file_name2_cls,
    )

