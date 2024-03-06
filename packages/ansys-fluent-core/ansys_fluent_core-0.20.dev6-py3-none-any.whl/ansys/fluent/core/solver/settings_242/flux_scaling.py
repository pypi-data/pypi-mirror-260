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

from .enabled_all import enabled_all as enabled_all_cls
from .disabled_all import disabled_all as disabled_all_cls
from .interface_name_2 import interface_name as interface_name_cls
from .scale_2 import scale as scale_cls
class flux_scaling(Command):
    """
    Enable or disable flux scaling at the turbo interfaces.
    
    Parameters
    ----------
        enabled_all : bool
            Enable flux scaling for all the interfaces.
        disabled_all : bool
            Disable flux scaling for all the interfaces.
        interface_name : str
            Define the turbo interface to enable/disable flux scaling.
        scale : bool
            Enable or disable flux scaling for the turbo interface.
    
    """

    fluent_name = "flux-scaling"

    argument_names = \
        ['enabled_all', 'disabled_all', 'interface_name', 'scale']

    _child_classes = dict(
        enabled_all=enabled_all_cls,
        disabled_all=disabled_all_cls,
        interface_name=interface_name_cls,
        scale=scale_cls,
    )

