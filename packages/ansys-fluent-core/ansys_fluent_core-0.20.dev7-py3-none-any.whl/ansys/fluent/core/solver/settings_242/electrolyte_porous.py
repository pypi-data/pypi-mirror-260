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

from .anode_interface import anode_interface as anode_interface_cls
from .cathode_interface import cathode_interface as cathode_interface_cls
from .tortuosity_interface import tortuosity_interface as tortuosity_interface_cls
from .pore_size_interface import pore_size_interface as pore_size_interface_cls
class electrolyte_porous(Group):
    """
    Enter electrolyte and porous zones settings.
    """

    fluent_name = "electrolyte-porous"

    child_names = \
        ['anode_interface', 'cathode_interface', 'tortuosity_interface',
         'pore_size_interface']

    _child_classes = dict(
        anode_interface=anode_interface_cls,
        cathode_interface=cathode_interface_cls,
        tortuosity_interface=tortuosity_interface_cls,
        pore_size_interface=pore_size_interface_cls,
    )

