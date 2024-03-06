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

from .file_name_2 import file_name as file_name_cls
class compute_write_vf(Command):
    """
    Compute and write both surface clusters and view factors.
    
    Parameters
    ----------
        file_name : str
            Name of output file for updated surface clusters and view factors.
    
    """

    fluent_name = "compute-write-vf"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

