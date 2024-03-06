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

from .cathode_i0 import cathode_i0 as cathode_i0_cls
from .cathode_alpha1 import cathode_alpha1 as cathode_alpha1_cls
from .cathode_alpha2 import cathode_alpha2 as cathode_alpha2_cls
from .cathode_alpha3 import cathode_alpha3 as cathode_alpha3_cls
from .cathode_alpha_a import cathode_alpha_a as cathode_alpha_a_cls
from .cathode_alpha_c import cathode_alpha_c as cathode_alpha_c_cls
from .cathode_ocv import cathode_ocv as cathode_ocv_cls
from .anode_i0 import anode_i0 as anode_i0_cls
from .anode_alpha1 import anode_alpha1 as anode_alpha1_cls
from .anode_alpha2 import anode_alpha2 as anode_alpha2_cls
from .anode_alpha3 import anode_alpha3 as anode_alpha3_cls
from .anode_alpha_a import anode_alpha_a as anode_alpha_a_cls
from .anode_alpha_c import anode_alpha_c as anode_alpha_c_cls
from .anode_ocv import anode_ocv as anode_ocv_cls
from .linearized_bv_rate import linearized_bv_rate as linearized_bv_rate_cls
class butler_volmer_rate(Group):
    """
    Set up Butler-Volmer rate kinetics parameters.
    """

    fluent_name = "butler-volmer-rate"

    child_names = \
        ['cathode_i0', 'cathode_alpha1', 'cathode_alpha2', 'cathode_alpha3',
         'cathode_alpha_a', 'cathode_alpha_c', 'cathode_ocv', 'anode_i0',
         'anode_alpha1', 'anode_alpha2', 'anode_alpha3', 'anode_alpha_a',
         'anode_alpha_c', 'anode_ocv', 'linearized_bv_rate']

    _child_classes = dict(
        cathode_i0=cathode_i0_cls,
        cathode_alpha1=cathode_alpha1_cls,
        cathode_alpha2=cathode_alpha2_cls,
        cathode_alpha3=cathode_alpha3_cls,
        cathode_alpha_a=cathode_alpha_a_cls,
        cathode_alpha_c=cathode_alpha_c_cls,
        cathode_ocv=cathode_ocv_cls,
        anode_i0=anode_i0_cls,
        anode_alpha1=anode_alpha1_cls,
        anode_alpha2=anode_alpha2_cls,
        anode_alpha3=anode_alpha3_cls,
        anode_alpha_a=anode_alpha_a_cls,
        anode_alpha_c=anode_alpha_c_cls,
        anode_ocv=anode_ocv_cls,
        linearized_bv_rate=linearized_bv_rate_cls,
    )

