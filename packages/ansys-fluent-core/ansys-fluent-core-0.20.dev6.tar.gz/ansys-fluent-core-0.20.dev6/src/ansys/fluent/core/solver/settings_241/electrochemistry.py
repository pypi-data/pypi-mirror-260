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

from .anode_alpha_a_2 import anode_alpha_a as anode_alpha_a_cls
from .anode_alpha_b import anode_alpha_b as anode_alpha_b_cls
from .cathode_alpha_a_2 import cathode_alpha_a as cathode_alpha_a_cls
from .cathode_alpha_b import cathode_alpha_b as cathode_alpha_b_cls
from .molef_ref_h2 import molef_ref_h2 as molef_ref_h2_cls
from .molef_ref_o2 import molef_ref_o2 as molef_ref_o2_cls
from .molef_ref_h2o import molef_ref_h2o as molef_ref_h2o_cls
from .exponent_h2 import exponent_h2 as exponent_h2_cls
from .exponent_o2 import exponent_o2 as exponent_o2_cls
from .exponent_h2o import exponent_h2o as exponent_h2o_cls
from .temp_depend_anode_i0 import temp_depend_anode_i0 as temp_depend_anode_i0_cls
from .temp_depend_cathode_i0 import temp_depend_cathode_i0 as temp_depend_cathode_i0_cls
from .anode_i0_2 import anode_i0 as anode_i0_cls
from .cathode_i0_2 import cathode_i0 as cathode_i0_cls
from .a_anode_i0 import a_anode_i0 as a_anode_i0_cls
from .b_anode_i0 import b_anode_i0 as b_anode_i0_cls
from .a_cathode_i0 import a_cathode_i0 as a_cathode_i0_cls
from .b_cathode_i0 import b_cathode_i0 as b_cathode_i0_cls
class electrochemistry(Group):
    """
    Electrochemistry.
    """

    fluent_name = "electrochemistry"

    child_names = \
        ['anode_alpha_a', 'anode_alpha_b', 'cathode_alpha_a',
         'cathode_alpha_b', 'molef_ref_h2', 'molef_ref_o2', 'molef_ref_h2o',
         'exponent_h2', 'exponent_o2', 'exponent_h2o', 'temp_depend_anode_i0',
         'temp_depend_cathode_i0', 'anode_i0', 'cathode_i0', 'a_anode_i0',
         'b_anode_i0', 'a_cathode_i0', 'b_cathode_i0']

    _child_classes = dict(
        anode_alpha_a=anode_alpha_a_cls,
        anode_alpha_b=anode_alpha_b_cls,
        cathode_alpha_a=cathode_alpha_a_cls,
        cathode_alpha_b=cathode_alpha_b_cls,
        molef_ref_h2=molef_ref_h2_cls,
        molef_ref_o2=molef_ref_o2_cls,
        molef_ref_h2o=molef_ref_h2o_cls,
        exponent_h2=exponent_h2_cls,
        exponent_o2=exponent_o2_cls,
        exponent_h2o=exponent_h2o_cls,
        temp_depend_anode_i0=temp_depend_anode_i0_cls,
        temp_depend_cathode_i0=temp_depend_cathode_i0_cls,
        anode_i0=anode_i0_cls,
        cathode_i0=cathode_i0_cls,
        a_anode_i0=a_anode_i0_cls,
        b_anode_i0=b_anode_i0_cls,
        a_cathode_i0=a_cathode_i0_cls,
        b_cathode_i0=b_cathode_i0_cls,
    )

