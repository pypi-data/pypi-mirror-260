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
from .max_val import max_val as max_val_cls
class set_maximum(Command):
    """
    'set_maximum' command.
    
    Parameters
    ----------
        sample_var : str
            'sample_var' child.
        max_val : real
            'max_val' child.
    
    """

    fluent_name = "set-maximum"

    argument_names = \
        ['sample_var', 'max_val']

    _child_classes = dict(
        sample_var=sample_var_cls,
        max_val=max_val_cls,
    )

