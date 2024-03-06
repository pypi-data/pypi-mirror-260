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
from .anode_cl_svratio import anode_cl_svratio as anode_cl_svratio_cls
from .anode_cl_thickness import anode_cl_thickness as anode_cl_thickness_cls
from .anode_cl_cp_function import anode_cl_cp_function as anode_cl_cp_function_cls
from .anode_cl_angle import anode_cl_angle as anode_cl_angle_cls
from .anode_cl_a import anode_cl_a as anode_cl_a_cls
from .anode_cl_b import anode_cl_b as anode_cl_b_cls
from .anode_cl_c import anode_cl_c as anode_cl_c_cls
class anode_cl_zone(Group):
    """
    Set up anode catalyst layer.
    """

    fluent_name = "anode-cl-zone"

    child_names = \
        ['anode_cl_zone_list', 'anode_cl_update', 'anode_cl_material',
         'anode_cl_porosity', 'anode_cl_kr', 'anode_cl_svratio',
         'anode_cl_thickness', 'anode_cl_cp_function', 'anode_cl_angle',
         'anode_cl_a', 'anode_cl_b', 'anode_cl_c']

    _child_classes = dict(
        anode_cl_zone_list=anode_cl_zone_list_cls,
        anode_cl_update=anode_cl_update_cls,
        anode_cl_material=anode_cl_material_cls,
        anode_cl_porosity=anode_cl_porosity_cls,
        anode_cl_kr=anode_cl_kr_cls,
        anode_cl_svratio=anode_cl_svratio_cls,
        anode_cl_thickness=anode_cl_thickness_cls,
        anode_cl_cp_function=anode_cl_cp_function_cls,
        anode_cl_angle=anode_cl_angle_cls,
        anode_cl_a=anode_cl_a_cls,
        anode_cl_b=anode_cl_b_cls,
        anode_cl_c=anode_cl_c_cls,
    )

