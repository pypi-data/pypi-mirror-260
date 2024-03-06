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

from .object_name_1 import object_name as object_name_cls
from .write_format import write_format as write_format_cls
from .file_name import file_name as file_name_cls
class write(Command):
    """
    'write' command.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
        write_format : str
            'write_format' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "write"

    argument_names = \
        ['object_name', 'write_format', 'file_name']

    _child_classes = dict(
        object_name=object_name_cls,
        write_format=write_format_cls,
        file_name=file_name_cls,
    )

