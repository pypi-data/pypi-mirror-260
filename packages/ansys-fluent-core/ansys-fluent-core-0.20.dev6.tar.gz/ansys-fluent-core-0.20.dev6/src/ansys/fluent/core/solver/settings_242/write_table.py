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

from .file_name_6 import file_name as file_name_cls
class write_table(Command):
    """
    2D table writting command.
    
    Parameters
    ----------
        file_name : str
            File name in 2D table writting.
    
    """

    fluent_name = "write-table"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

