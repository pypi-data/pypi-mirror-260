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

from .anode_pl_zone_list import anode_pl_zone_list as anode_pl_zone_list_cls
from .anode_pl_update import anode_pl_update as anode_pl_update_cls
from .anode_pl_material import anode_pl_material as anode_pl_material_cls
from .anode_pl_porosity import anode_pl_porosity as anode_pl_porosity_cls
from .anode_pl_kr import anode_pl_kr as anode_pl_kr_cls
class anode_pl_zone(Group):
    """
    'anode_pl_zone' child.
    """

    fluent_name = "anode-pl-zone"

    child_names = \
        ['anode_pl_zone_list', 'anode_pl_update', 'anode_pl_material',
         'anode_pl_porosity', 'anode_pl_kr']

    _child_classes = dict(
        anode_pl_zone_list=anode_pl_zone_list_cls,
        anode_pl_update=anode_pl_update_cls,
        anode_pl_material=anode_pl_material_cls,
        anode_pl_porosity=anode_pl_porosity_cls,
        anode_pl_kr=anode_pl_kr_cls,
    )

