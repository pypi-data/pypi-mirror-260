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

from .file_type import file_type as file_type_cls
from .file_name_1 import file_name as file_name_cls
class write(Command):
    """
    'write' command.
    
    Parameters
    ----------
        file_type : str
            'file_type' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "write"

    argument_names = \
        ['file_type', 'file_name']

    _child_classes = dict(
        file_type=file_type_cls,
        file_name=file_name_cls,
    )

