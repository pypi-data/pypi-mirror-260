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

from .sample_file import sample_file as sample_file_cls
class read_sample_file(Command):
    """
    Read a sample file and add it to the sample list.
    
    Parameters
    ----------
        sample_file : str
            Enter the name of a sample file to be loaded.
    
    """

    fluent_name = "read-sample-file"

    argument_names = \
        ['sample_file']

    _child_classes = dict(
        sample_file=sample_file_cls,
    )

