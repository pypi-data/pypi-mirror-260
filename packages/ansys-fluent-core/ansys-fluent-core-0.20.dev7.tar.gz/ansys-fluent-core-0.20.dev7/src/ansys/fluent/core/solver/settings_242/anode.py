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
from .anode_fc_zone import anode_fc_zone as anode_fc_zone_cls
from .anode_pl_zone import anode_pl_zone as anode_pl_zone_cls
from .anode_cl_zone import anode_cl_zone as anode_cl_zone_cls
class anode(Group):
    """
    Set up anode.
    """

    fluent_name = "anode"

    child_names = \
        ['anode_cc_zone', 'anode_fc_zone', 'anode_pl_zone', 'anode_cl_zone']

    _child_classes = dict(
        anode_cc_zone=anode_cc_zone_cls,
        anode_fc_zone=anode_fc_zone_cls,
        anode_pl_zone=anode_pl_zone_cls,
        anode_cl_zone=anode_cl_zone_cls,
    )

