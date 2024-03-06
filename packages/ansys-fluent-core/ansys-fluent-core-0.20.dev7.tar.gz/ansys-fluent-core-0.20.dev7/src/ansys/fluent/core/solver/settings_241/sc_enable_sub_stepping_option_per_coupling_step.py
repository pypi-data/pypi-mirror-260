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

from .enable_sub_stepping import enable_sub_stepping as enable_sub_stepping_cls
from .num_sub_stepping_coupling_itr import num_sub_stepping_coupling_itr as num_sub_stepping_coupling_itr_cls
class sc_enable_sub_stepping_option_per_coupling_step(Command):
    """
    Enable/disable sub stepping option per coupling step.
    
    Parameters
    ----------
        enable_sub_stepping : bool
            Enable or Disable sub stepping options for each coupling  steps.
        num_sub_stepping_coupling_itr : int
            Set the number of substeps for each coupling iterations (default = 1).
    
    """

    fluent_name = "sc-enable-sub-stepping-option-per-coupling-step"

    argument_names = \
        ['enable_sub_stepping', 'num_sub_stepping_coupling_itr']

    _child_classes = dict(
        enable_sub_stepping=enable_sub_stepping_cls,
        num_sub_stepping_coupling_itr=num_sub_stepping_coupling_itr_cls,
    )

