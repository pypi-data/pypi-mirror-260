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

from .check_reduction_wt import check_reduction_wt as check_reduction_wt_cls
from .file_name_1 import file_name as file_name_cls
class reduce_picked_sample(Command):
    """
    Reduce a sample after first picking it and setting up all data-reduction options and parameters.
    
    Parameters
    ----------
        check_reduction_wt : bool
            'check_reduction_wt' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "reduce-picked-sample"

    argument_names = \
        ['check_reduction_wt', 'file_name']

    _child_classes = dict(
        check_reduction_wt=check_reduction_wt_cls,
        file_name=file_name_cls,
    )

