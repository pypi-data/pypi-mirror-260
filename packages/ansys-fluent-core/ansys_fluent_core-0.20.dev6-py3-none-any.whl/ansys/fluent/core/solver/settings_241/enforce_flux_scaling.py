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

from .enable_scale_all import enable_scale_all as enable_scale_all_cls
from .disable_scale_all import disable_scale_all as disable_scale_all_cls
from .interface_name_2 import interface_name as interface_name_cls
from .scale_2 import scale as scale_cls
class enforce_flux_scaling(Command):
    """
    Enforce flux scaling ON/OFF at the turbo interfaces.
    
    Parameters
    ----------
        enable_scale_all : bool
            Scale scaling of all the interfaces...
        disable_scale_all : bool
            Disable scaling of all the interfaces...
        interface_name : str
            'interface_name' child.
        scale : bool
            Enable flux scaling at mixing plane interface.
    
    """

    fluent_name = "enforce-flux-scaling"

    argument_names = \
        ['enable_scale_all', 'disable_scale_all', 'interface_name', 'scale']

    _child_classes = dict(
        enable_scale_all=enable_scale_all_cls,
        disable_scale_all=disable_scale_all_cls,
        interface_name=interface_name_cls,
        scale=scale_cls,
    )

