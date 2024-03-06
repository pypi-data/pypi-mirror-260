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

from .cathode_pl_zone_list import cathode_pl_zone_list as cathode_pl_zone_list_cls
from .cathode_pl_update import cathode_pl_update as cathode_pl_update_cls
from .cathode_pl_material import cathode_pl_material as cathode_pl_material_cls
from .cathode_pl_porosity import cathode_pl_porosity as cathode_pl_porosity_cls
from .cathode_pl_kr import cathode_pl_kr as cathode_pl_kr_cls
from .cathode_pl_cp_function import cathode_pl_cp_function as cathode_pl_cp_function_cls
from .cathode_pl_angle import cathode_pl_angle as cathode_pl_angle_cls
from .cathode_pl_a import cathode_pl_a as cathode_pl_a_cls
from .cathode_pl_b import cathode_pl_b as cathode_pl_b_cls
from .cathode_pl_c import cathode_pl_c as cathode_pl_c_cls
class cathode_pl_zone(Group):
    """
    Set up cathode porous layer.
    """

    fluent_name = "cathode-pl-zone"

    child_names = \
        ['cathode_pl_zone_list', 'cathode_pl_update', 'cathode_pl_material',
         'cathode_pl_porosity', 'cathode_pl_kr', 'cathode_pl_cp_function',
         'cathode_pl_angle', 'cathode_pl_a', 'cathode_pl_b', 'cathode_pl_c']

    _child_classes = dict(
        cathode_pl_zone_list=cathode_pl_zone_list_cls,
        cathode_pl_update=cathode_pl_update_cls,
        cathode_pl_material=cathode_pl_material_cls,
        cathode_pl_porosity=cathode_pl_porosity_cls,
        cathode_pl_kr=cathode_pl_kr_cls,
        cathode_pl_cp_function=cathode_pl_cp_function_cls,
        cathode_pl_angle=cathode_pl_angle_cls,
        cathode_pl_a=cathode_pl_a_cls,
        cathode_pl_b=cathode_pl_b_cls,
        cathode_pl_c=cathode_pl_c_cls,
    )

