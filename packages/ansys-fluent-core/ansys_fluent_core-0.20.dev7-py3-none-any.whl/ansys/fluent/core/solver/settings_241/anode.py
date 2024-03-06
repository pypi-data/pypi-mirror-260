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
from .anode_pl_cp_function import anode_pl_cp_function as anode_pl_cp_function_cls
from .anode_pl_angle import anode_pl_angle as anode_pl_angle_cls
from .anode_pl_a import anode_pl_a as anode_pl_a_cls
from .anode_pl_b import anode_pl_b as anode_pl_b_cls
from .anode_pl_c import anode_pl_c as anode_pl_c_cls
from .anode_cl_zone import anode_cl_zone as anode_cl_zone_cls
from .anode_cl_svratio import anode_cl_svratio as anode_cl_svratio_cls
from .anode_cl_thickness import anode_cl_thickness as anode_cl_thickness_cls
from .anode_cl_cp_function import anode_cl_cp_function as anode_cl_cp_function_cls
from .anode_cl_angle import anode_cl_angle as anode_cl_angle_cls
from .anode_cl_a import anode_cl_a as anode_cl_a_cls
from .anode_cl_b import anode_cl_b as anode_cl_b_cls
from .anode_cl_c import anode_cl_c as anode_cl_c_cls
class anode(Group):
    """
    'anode' child.
    """

    fluent_name = "anode"

    child_names = \
        ['anode_cc_zone', 'anode_fc_zone', 'anode_pl_zone',
         'anode_pl_cp_function', 'anode_pl_angle', 'anode_pl_a', 'anode_pl_b',
         'anode_pl_c', 'anode_cl_zone', 'anode_cl_svratio',
         'anode_cl_thickness', 'anode_cl_cp_function', 'anode_cl_angle',
         'anode_cl_a', 'anode_cl_b', 'anode_cl_c']

    _child_classes = dict(
        anode_cc_zone=anode_cc_zone_cls,
        anode_fc_zone=anode_fc_zone_cls,
        anode_pl_zone=anode_pl_zone_cls,
        anode_pl_cp_function=anode_pl_cp_function_cls,
        anode_pl_angle=anode_pl_angle_cls,
        anode_pl_a=anode_pl_a_cls,
        anode_pl_b=anode_pl_b_cls,
        anode_pl_c=anode_pl_c_cls,
        anode_cl_zone=anode_cl_zone_cls,
        anode_cl_svratio=anode_cl_svratio_cls,
        anode_cl_thickness=anode_cl_thickness_cls,
        anode_cl_cp_function=anode_cl_cp_function_cls,
        anode_cl_angle=anode_cl_angle_cls,
        anode_cl_a=anode_cl_a_cls,
        anode_cl_b=anode_cl_b_cls,
        anode_cl_c=anode_cl_c_cls,
    )

