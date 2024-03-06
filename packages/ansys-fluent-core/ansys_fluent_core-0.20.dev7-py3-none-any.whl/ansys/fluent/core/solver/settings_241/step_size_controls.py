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

from .option_6 import option as option_cls
from .length_scale import length_scale as length_scale_cls
from .step_length_factor import step_length_factor as step_length_factor_cls
class step_size_controls(Group):
    """
    Main menu to control the time integration of the particle trajectory equations:
    
     - the maximum number of steps; the trajectory calculation is stopped and the particle aborted when the particle reaches this limit.
     - the length scale/step length factor; this factor is used to set the time step size for integration within a cell.
    
    """

    fluent_name = "step-size-controls"

    child_names = \
        ['option', 'length_scale', 'step_length_factor']

    _child_classes = dict(
        option=option_cls,
        length_scale=length_scale_cls,
        step_length_factor=step_length_factor_cls,
    )

