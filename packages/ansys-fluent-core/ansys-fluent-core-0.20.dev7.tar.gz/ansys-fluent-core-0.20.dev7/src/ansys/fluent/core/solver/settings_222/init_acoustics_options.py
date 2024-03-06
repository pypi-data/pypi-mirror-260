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

from .set_ramping_length import set_ramping_length as set_ramping_length_cls
from .number_of_timesteps import number_of_timesteps as number_of_timesteps_cls
class init_acoustics_options(Command):
    """
    'init_acoustics_options' command.
    
    Parameters
    ----------
        set_ramping_length : bool
            Enable/Disable ramping length and initialize acoustics.
        number_of_timesteps : int
            Set number of timesteps for ramping of sources.
    
    """

    fluent_name = "init-acoustics-options"

    argument_names = \
        ['set_ramping_length', 'number_of_timesteps']

    _child_classes = dict(
        set_ramping_length=set_ramping_length_cls,
        number_of_timesteps=number_of_timesteps_cls,
    )

