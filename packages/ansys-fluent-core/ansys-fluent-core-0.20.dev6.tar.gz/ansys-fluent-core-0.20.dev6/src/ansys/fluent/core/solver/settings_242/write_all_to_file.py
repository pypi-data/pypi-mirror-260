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
from .append_data import append_data as append_data_cls
class write_all_to_file(Command):
    """
    Write all parameters value to file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
    
    """

    fluent_name = "write-all-to-file"

    argument_names = \
        ['file_name', 'append_data']

    _child_classes = dict(
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

