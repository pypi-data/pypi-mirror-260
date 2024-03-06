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
class bv_symmetry_factor(Group):
    """
    Enter the Butler-Volmer symmetriy factors settings.
    """

    fluent_name = "bv-symmetry-factor"

    child_names = \
        ['anode_alpha_a', 'anode_alpha_b', 'cathode_alpha_a',
         'cathode_alpha_b']

    _child_classes = dict(
        anode_alpha_a=anode_alpha_a_cls,
        anode_alpha_b=anode_alpha_b_cls,
        cathode_alpha_a=cathode_alpha_a_cls,
        cathode_alpha_b=cathode_alpha_b_cls,
    )

