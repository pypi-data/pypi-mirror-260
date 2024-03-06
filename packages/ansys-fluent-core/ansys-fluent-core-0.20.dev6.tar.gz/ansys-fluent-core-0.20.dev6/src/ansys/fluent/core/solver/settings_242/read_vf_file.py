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

from .file_name_1_2 import file_name_1 as file_name_1_cls
class read_vf_file(Command):
    """
    Read an S2S file.
    
    Parameters
    ----------
        file_name_1 : str
            Name of input file containing view factors.
    
    """

    fluent_name = "read-vf-file"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_1_cls,
    )

