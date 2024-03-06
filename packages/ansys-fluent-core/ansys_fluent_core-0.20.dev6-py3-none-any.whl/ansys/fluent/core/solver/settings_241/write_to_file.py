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

from .filename_3 import filename as filename_cls
class write_to_file(Command):
    """
    Write data to file.
    
    Parameters
    ----------
        filename : str
            Enter file name.
    
    """

    fluent_name = "write-to-file"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

