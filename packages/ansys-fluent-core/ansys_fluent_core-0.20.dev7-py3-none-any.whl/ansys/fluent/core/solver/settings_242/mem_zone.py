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

from .mem_zone_list import mem_zone_list as mem_zone_list_cls
from .mem_update import mem_update as mem_update_cls
from .mem_material import mem_material as mem_material_cls
from .mem_porosity import mem_porosity as mem_porosity_cls
from .mem_kr import mem_kr as mem_kr_cls
class mem_zone(Group):
    """
    Set up electrolyte cell zones.
    """

    fluent_name = "mem-zone"

    child_names = \
        ['mem_zone_list', 'mem_update', 'mem_material', 'mem_porosity',
         'mem_kr']

    _child_classes = dict(
        mem_zone_list=mem_zone_list_cls,
        mem_update=mem_update_cls,
        mem_material=mem_material_cls,
        mem_porosity=mem_porosity_cls,
        mem_kr=mem_kr_cls,
    )

