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
from .min_val import min_val as min_val_cls
class set_minimum(Command):
    """
    Set the minimum value of the range to be considered for a specific variable in the data reduction.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        min_val : real
            'min_val' child.
    
    """

    fluent_name = "set-minimum"

    argument_names = \
        ['sample_var', 'min_val']

    _child_classes = dict(
        sample_var=sample_var_cls,
        min_val=min_val_cls,
    )

