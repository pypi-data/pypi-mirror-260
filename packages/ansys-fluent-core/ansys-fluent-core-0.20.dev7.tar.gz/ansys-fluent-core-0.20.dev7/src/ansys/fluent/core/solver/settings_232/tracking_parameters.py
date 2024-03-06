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

from .control_by import control_by as control_by_cls
from .max_number_of_steps import max_number_of_steps as max_number_of_steps_cls
from .length_scale import length_scale as length_scale_cls
from .step_length_factor import step_length_factor as step_length_factor_cls
class tracking_parameters(Group):
    """
    Main menu to control the time integration of the particle trajectory equations:
    
     - the maximum number of steps; the trajectory calculation is stopped and the particle aborted when the particle reaches this limit.
     - the length scale/step length factor; this factor is used to set the time step size for integration within a cell.
    
    """

    fluent_name = "tracking-parameters"

    child_names = \
        ['control_by', 'max_number_of_steps', 'length_scale',
         'step_length_factor']

    _child_classes = dict(
        control_by=control_by_cls,
        max_number_of_steps=max_number_of_steps_cls,
        length_scale=length_scale_cls,
        step_length_factor=step_length_factor_cls,
    )

