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

from .file_name import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls
class write_sc_file(Command):
    """
    Write a Fluent Input File for System Coupling.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "write-sc-file"

    argument_names = \
        ['file_name', 'overwrite']

    _child_classes = dict(
        file_name=file_name_cls,
        overwrite=overwrite_cls,
    )

