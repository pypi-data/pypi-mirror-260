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

from .temp_depend_anode_i0 import temp_depend_anode_i0 as temp_depend_anode_i0_cls
from .temp_depend_cathode_i0 import temp_depend_cathode_i0 as temp_depend_cathode_i0_cls
from .anode_i0_2 import anode_i0 as anode_i0_cls
from .cathode_i0_2 import cathode_i0 as cathode_i0_cls
from .a_anode_i0 import a_anode_i0 as a_anode_i0_cls
from .b_anode_i0 import b_anode_i0 as b_anode_i0_cls
from .a_cathode_i0 import a_cathode_i0 as a_cathode_i0_cls
from .b_cathode_i0 import b_cathode_i0 as b_cathode_i0_cls
class exchange_current(Group):
    """
    Enter the exchange current density settings.
    """

    fluent_name = "exchange-current"

    child_names = \
        ['temp_depend_anode_i0', 'temp_depend_cathode_i0', 'anode_i0',
         'cathode_i0', 'a_anode_i0', 'b_anode_i0', 'a_cathode_i0',
         'b_cathode_i0']

    _child_classes = dict(
        temp_depend_anode_i0=temp_depend_anode_i0_cls,
        temp_depend_cathode_i0=temp_depend_cathode_i0_cls,
        anode_i0=anode_i0_cls,
        cathode_i0=cathode_i0_cls,
        a_anode_i0=a_anode_i0_cls,
        b_anode_i0=b_anode_i0_cls,
        a_cathode_i0=a_cathode_i0_cls,
        b_cathode_i0=b_cathode_i0_cls,
    )

