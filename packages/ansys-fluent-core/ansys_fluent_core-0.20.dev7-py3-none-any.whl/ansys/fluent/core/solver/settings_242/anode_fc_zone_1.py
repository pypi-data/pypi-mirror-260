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

from .anode_fc_zone_list import anode_fc_zone_list as anode_fc_zone_list_cls
from .anode_fc_condensation import anode_fc_condensation as anode_fc_condensation_cls
from .anode_fc_evaporation import anode_fc_evaporation as anode_fc_evaporation_cls
class anode_fc_zone(Group):
    """
    Set up anode flow channel.
    """

    fluent_name = "anode-fc-zone"

    child_names = \
        ['anode_fc_zone_list', 'anode_fc_condensation',
         'anode_fc_evaporation']

    _child_classes = dict(
        anode_fc_zone_list=anode_fc_zone_list_cls,
        anode_fc_condensation=anode_fc_condensation_cls,
        anode_fc_evaporation=anode_fc_evaporation_cls,
    )

