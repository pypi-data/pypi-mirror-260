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

from .cathode_cc_zone import cathode_cc_zone as cathode_cc_zone_cls
from .cathode_fc_zone import cathode_fc_zone as cathode_fc_zone_cls
from .cathode_pl_zone import cathode_pl_zone as cathode_pl_zone_cls
from .cathode_pl_cp_function import cathode_pl_cp_function as cathode_pl_cp_function_cls
from .cathode_pl_angle import cathode_pl_angle as cathode_pl_angle_cls
from .cathode_pl_a import cathode_pl_a as cathode_pl_a_cls
from .cathode_pl_b import cathode_pl_b as cathode_pl_b_cls
from .cathode_pl_c import cathode_pl_c as cathode_pl_c_cls
from .cathode_cl_zone import cathode_cl_zone as cathode_cl_zone_cls
from .cathode_cl_svratio import cathode_cl_svratio as cathode_cl_svratio_cls
from .cathode_cl_thickness import cathode_cl_thickness as cathode_cl_thickness_cls
from .cathode_cl_cp_function import cathode_cl_cp_function as cathode_cl_cp_function_cls
from .cathode_cl_angle import cathode_cl_angle as cathode_cl_angle_cls
from .cathode_cl_a import cathode_cl_a as cathode_cl_a_cls
from .cathode_cl_b import cathode_cl_b as cathode_cl_b_cls
from .cathode_cl_c import cathode_cl_c as cathode_cl_c_cls
class cathode(Group):
    """
    'cathode' child.
    """

    fluent_name = "cathode"

    child_names = \
        ['cathode_cc_zone', 'cathode_fc_zone', 'cathode_pl_zone',
         'cathode_pl_cp_function', 'cathode_pl_angle', 'cathode_pl_a',
         'cathode_pl_b', 'cathode_pl_c', 'cathode_cl_zone',
         'cathode_cl_svratio', 'cathode_cl_thickness',
         'cathode_cl_cp_function', 'cathode_cl_angle', 'cathode_cl_a',
         'cathode_cl_b', 'cathode_cl_c']

    _child_classes = dict(
        cathode_cc_zone=cathode_cc_zone_cls,
        cathode_fc_zone=cathode_fc_zone_cls,
        cathode_pl_zone=cathode_pl_zone_cls,
        cathode_pl_cp_function=cathode_pl_cp_function_cls,
        cathode_pl_angle=cathode_pl_angle_cls,
        cathode_pl_a=cathode_pl_a_cls,
        cathode_pl_b=cathode_pl_b_cls,
        cathode_pl_c=cathode_pl_c_cls,
        cathode_cl_zone=cathode_cl_zone_cls,
        cathode_cl_svratio=cathode_cl_svratio_cls,
        cathode_cl_thickness=cathode_cl_thickness_cls,
        cathode_cl_cp_function=cathode_cl_cp_function_cls,
        cathode_cl_angle=cathode_cl_angle_cls,
        cathode_cl_a=cathode_cl_a_cls,
        cathode_cl_b=cathode_cl_b_cls,
        cathode_cl_c=cathode_cl_c_cls,
    )

