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

from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_of_moments import num_of_moments as num_of_moments_cls
from .write_to_file import write_to_file as write_to_file_cls
from .filename import filename as filename_cls
from .overwrite import overwrite as overwrite_cls
class moments(Command):
    """
    Set moments for population balance.
    
    Parameters
    ----------
        surface_list : typing.List[str]
            'surface_list' child.
        volume_list : typing.List[str]
            'volume_list' child.
        num_of_moments : int
            'num_of_moments' child.
        write_to_file : bool
            'write_to_file' child.
        filename : str
            'filename' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "moments"

    argument_names = \
        ['surface_list', 'volume_list', 'num_of_moments', 'write_to_file',
         'filename', 'overwrite']

    _child_classes = dict(
        surface_list=surface_list_cls,
        volume_list=volume_list_cls,
        num_of_moments=num_of_moments_cls,
        write_to_file=write_to_file_cls,
        filename=filename_cls,
        overwrite=overwrite_cls,
    )

