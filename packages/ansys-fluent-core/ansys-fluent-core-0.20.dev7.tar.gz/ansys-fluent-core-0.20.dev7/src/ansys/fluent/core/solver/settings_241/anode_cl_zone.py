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

from .anode_cl_zone_list import anode_cl_zone_list as anode_cl_zone_list_cls
from .anode_cl_update import anode_cl_update as anode_cl_update_cls
from .anode_cl_material import anode_cl_material as anode_cl_material_cls
from .anode_cl_porosity import anode_cl_porosity as anode_cl_porosity_cls
from .anode_cl_kr import anode_cl_kr as anode_cl_kr_cls
class anode_cl_zone(Group):
    """
    'anode_cl_zone' child.
    """

    fluent_name = "anode-cl-zone"

    child_names = \
        ['anode_cl_zone_list', 'anode_cl_update', 'anode_cl_material',
         'anode_cl_porosity', 'anode_cl_kr']

    _child_classes = dict(
        anode_cl_zone_list=anode_cl_zone_list_cls,
        anode_cl_update=anode_cl_update_cls,
        anode_cl_material=anode_cl_material_cls,
        anode_cl_porosity=anode_cl_porosity_cls,
        anode_cl_kr=anode_cl_kr_cls,
    )

