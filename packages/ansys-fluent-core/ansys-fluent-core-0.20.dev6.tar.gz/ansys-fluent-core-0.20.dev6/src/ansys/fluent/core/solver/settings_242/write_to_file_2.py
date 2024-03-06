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

from .file_name_10 import file_name as file_name_cls
class write_to_file(Command):
    """
    Write number density report to file.
    
    Parameters
    ----------
        file_name : str
            Enter file name to write number density report.
    
    """

    fluent_name = "write-to-file"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

