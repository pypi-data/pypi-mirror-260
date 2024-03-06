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

from .enabled_all_1 import enabled_all as enabled_all_cls
from .disabled_all_1 import disabled_all as disabled_all_cls
from .interface_name_3 import interface_name as interface_name_cls
from .nps_min_po_loss import nps_min_po_loss as nps_min_po_loss_cls
class nps_minimize_po_loss(Command):
    """
    Enable or disable minimize total pressure loss option for the nps interfaces.
    
    Parameters
    ----------
        enabled_all : bool
            Enable for all the nps interfaces.
        disabled_all : bool
            Disable for all the nps interfaces.
        interface_name : str
            Define the nps interface to enable/disable minimize total pressure loss option.
        nps_min_po_loss : bool
            Enable or disable minimize total pressure loss option for the specified interface.
    
    """

    fluent_name = "nps-minimize-po-loss"

    argument_names = \
        ['enabled_all', 'disabled_all', 'interface_name', 'nps_min_po_loss']

    _child_classes = dict(
        enabled_all=enabled_all_cls,
        disabled_all=disabled_all_cls,
        interface_name=interface_name_cls,
        nps_min_po_loss=nps_min_po_loss_cls,
    )

