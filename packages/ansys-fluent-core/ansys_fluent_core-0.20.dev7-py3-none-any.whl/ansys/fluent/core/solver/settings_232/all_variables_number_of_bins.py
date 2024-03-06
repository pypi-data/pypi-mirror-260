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

from .all_var_num_of_bins import all_var_num_of_bins as all_var_num_of_bins_cls
class all_variables_number_of_bins(Command):
    """
    Set the number of bins to be used for ALL variables in the data reduction.
    
    Parameters
    ----------
        all_var_num_of_bins : int
            'all_var_num_of_bins' child.
    
    """

    fluent_name = "all-variables-number-of-bins"

    argument_names = \
        ['all_var_num_of_bins']

    _child_classes = dict(
        all_var_num_of_bins=all_var_num_of_bins_cls,
    )

