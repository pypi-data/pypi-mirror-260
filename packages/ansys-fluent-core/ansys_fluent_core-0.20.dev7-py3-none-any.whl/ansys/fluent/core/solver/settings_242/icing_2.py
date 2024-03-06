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

from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .fensapice_ice_icing_mode import fensapice_ice_icing_mode as fensapice_ice_icing_mode_cls
from .fensapice_ice_hflux import fensapice_ice_hflux as fensapice_ice_hflux_cls
from .fensapice_ice_hflux_1 import fensapice_ice_hflux_1 as fensapice_ice_hflux_1_cls
from .fensapice_drop_vwet import fensapice_drop_vwet as fensapice_drop_vwet_cls
from .fensapice_drop_reinj import fensapice_drop_reinj as fensapice_drop_reinj_cls
from .fensapice_dpm_wall_condition import fensapice_dpm_wall_condition as fensapice_dpm_wall_condition_cls
from .fensapice_dpm_bc_norm_coeff import fensapice_dpm_bc_norm_coeff as fensapice_dpm_bc_norm_coeff_cls
from .fensapice_dpm_bc_tang_coeff import fensapice_dpm_bc_tang_coeff as fensapice_dpm_bc_tang_coeff_cls
class icing(Group):
    """
    Help not available.
    """

    fluent_name = "icing"

    child_names = \
        ['fensapice_flow_bc_subtype', 'fensapice_ice_icing_mode',
         'fensapice_ice_hflux', 'fensapice_ice_hflux_1',
         'fensapice_drop_vwet', 'fensapice_drop_reinj',
         'fensapice_dpm_wall_condition', 'fensapice_dpm_bc_norm_coeff',
         'fensapice_dpm_bc_tang_coeff']

    _child_classes = dict(
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        fensapice_ice_icing_mode=fensapice_ice_icing_mode_cls,
        fensapice_ice_hflux=fensapice_ice_hflux_cls,
        fensapice_ice_hflux_1=fensapice_ice_hflux_1_cls,
        fensapice_drop_vwet=fensapice_drop_vwet_cls,
        fensapice_drop_reinj=fensapice_drop_reinj_cls,
        fensapice_dpm_wall_condition=fensapice_dpm_wall_condition_cls,
        fensapice_dpm_bc_norm_coeff=fensapice_dpm_bc_norm_coeff_cls,
        fensapice_dpm_bc_tang_coeff=fensapice_dpm_bc_tang_coeff_cls,
    )

