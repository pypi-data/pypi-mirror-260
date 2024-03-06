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

from .file_name_3 import file_name as file_name_cls
class compute_vf_accelerated(Command):
    """
    Compute and write only view factors from existing surface clusters with GPU-acceleration.
    
    Parameters
    ----------
        file_name : str
            Name of output file for S2S view factors from existing surface clusters with GPU-acceleration.
    
    """

    fluent_name = "compute-vf-accelerated"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

