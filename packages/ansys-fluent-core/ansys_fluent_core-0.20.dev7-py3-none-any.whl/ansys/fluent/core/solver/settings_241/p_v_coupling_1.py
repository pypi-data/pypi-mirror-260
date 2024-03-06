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

from .coupled_vof import coupled_vof as coupled_vof_cls
from .rhie_chow_flux import rhie_chow_flux as rhie_chow_flux_cls
from .skewness_correction import skewness_correction as skewness_correction_cls
class p_v_coupling(Group):
    """
    Pressure velocity coupling controls for multiphase flow.
    """

    fluent_name = "p-v-coupling"

    child_names = \
        ['coupled_vof', 'rhie_chow_flux', 'skewness_correction']

    _child_classes = dict(
        coupled_vof=coupled_vof_cls,
        rhie_chow_flux=rhie_chow_flux_cls,
        skewness_correction=skewness_correction_cls,
    )

