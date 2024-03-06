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

from .enabled_30 import enabled as enabled_cls
from .option_name import option_name as option_name_cls
class transfer_motion_across_interfaces(Command):
    """
    Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
    
    Parameters
    ----------
        enabled : bool
            Enable motion transfer across mesh interfaces?.
        option_name : str
            Enter transfer type.
    
    """

    fluent_name = "transfer-motion-across-interfaces?"

    argument_names = \
        ['enabled', 'option_name']

    _child_classes = dict(
        enabled=enabled_cls,
        option_name=option_name_cls,
    )

