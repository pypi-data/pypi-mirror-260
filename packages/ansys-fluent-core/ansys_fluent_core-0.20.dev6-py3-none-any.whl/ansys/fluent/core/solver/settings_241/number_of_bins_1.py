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

from .sample_var import sample_var as sample_var_cls
from .num_bins import num_bins as num_bins_cls
class number_of_bins(Command):
    """
    Set the number of bins to be used for a specific variable in the data reduction.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        num_bins : int
            'num_bins' child.
    
    """

    fluent_name = "number-of-bins"

    argument_names = \
        ['sample_var', 'num_bins']

    _child_classes = dict(
        sample_var=sample_var_cls,
        num_bins=num_bins_cls,
    )

