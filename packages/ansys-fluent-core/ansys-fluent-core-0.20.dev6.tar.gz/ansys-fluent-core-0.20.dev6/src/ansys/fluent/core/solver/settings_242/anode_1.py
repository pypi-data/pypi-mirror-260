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

from .anode_cc_zone import anode_cc_zone as anode_cc_zone_cls
from .anode_fc_zone_1 import anode_fc_zone as anode_fc_zone_cls
from .anode_gdl_zone import anode_gdl_zone as anode_gdl_zone_cls
from .anode_mpl_zone import anode_mpl_zone as anode_mpl_zone_cls
from .anode_ca_zone import anode_ca_zone as anode_ca_zone_cls
class anode(Group):
    """
    Set up anode.
    """

    fluent_name = "anode"

    child_names = \
        ['anode_cc_zone', 'anode_fc_zone', 'anode_gdl_zone', 'anode_mpl_zone',
         'anode_ca_zone']

    _child_classes = dict(
        anode_cc_zone=anode_cc_zone_cls,
        anode_fc_zone=anode_fc_zone_cls,
        anode_gdl_zone=anode_gdl_zone_cls,
        anode_mpl_zone=anode_mpl_zone_cls,
        anode_ca_zone=anode_ca_zone_cls,
    )

