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

from .exchange_current import exchange_current as exchange_current_cls
from .mole_fraction_ref import mole_fraction_ref as mole_fraction_ref_cls
from .concentration_exp import concentration_exp as concentration_exp_cls
from .bv_symmetry_factor import bv_symmetry_factor as bv_symmetry_factor_cls
class electrochemistry(Group):
    """
    Enter the electrochemistry settings.
    """

    fluent_name = "electrochemistry"

    child_names = \
        ['exchange_current', 'mole_fraction_ref', 'concentration_exp',
         'bv_symmetry_factor']

    _child_classes = dict(
        exchange_current=exchange_current_cls,
        mole_fraction_ref=mole_fraction_ref_cls,
        concentration_exp=concentration_exp_cls,
        bv_symmetry_factor=bv_symmetry_factor_cls,
    )

