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

from .filename_1_3 import filename_1 as filename_1_cls
class write_to_file(Command):
    """
    Write data to file.
    
    Parameters
    ----------
        filename_1 : str
            Enter file name.
    
    """

    fluent_name = "write-to-file"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_1_cls,
    )

