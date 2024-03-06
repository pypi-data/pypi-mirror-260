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
from .fensapice_drop_bccustom import fensapice_drop_bccustom as fensapice_drop_bccustom_cls
from .fensapice_drop_lwc import fensapice_drop_lwc as fensapice_drop_lwc_cls
from .fensapice_drop_dtemp import fensapice_drop_dtemp as fensapice_drop_dtemp_cls
from .fensapice_drop_ddiam import fensapice_drop_ddiam as fensapice_drop_ddiam_cls
from .fensapice_drop_dv import fensapice_drop_dv as fensapice_drop_dv_cls
from .fensapice_drop_dx import fensapice_drop_dx as fensapice_drop_dx_cls
from .fensapice_drop_dy import fensapice_drop_dy as fensapice_drop_dy_cls
from .fensapice_drop_dz import fensapice_drop_dz as fensapice_drop_dz_cls
from .fensapice_dpm_surface_injection import fensapice_dpm_surface_injection as fensapice_dpm_surface_injection_cls
from .fensapice_dpm_inj_nstream import fensapice_dpm_inj_nstream as fensapice_dpm_inj_nstream_cls
from .fensapice_drop_icc import fensapice_drop_icc as fensapice_drop_icc_cls
from .fensapice_drop_ctemp import fensapice_drop_ctemp as fensapice_drop_ctemp_cls
from .fensapice_drop_cmelt import fensapice_drop_cmelt as fensapice_drop_cmelt_cls
from .fensapice_drop_cdiam import fensapice_drop_cdiam as fensapice_drop_cdiam_cls
from .fensapice_drop_cv import fensapice_drop_cv as fensapice_drop_cv_cls
from .fensapice_drop_cx import fensapice_drop_cx as fensapice_drop_cx_cls
from .fensapice_drop_cy import fensapice_drop_cy as fensapice_drop_cy_cls
from .fensapice_drop_cz import fensapice_drop_cz as fensapice_drop_cz_cls
from .fensapice_drop_vrh import fensapice_drop_vrh as fensapice_drop_vrh_cls
from .fensapice_drop_vrh_1 import fensapice_drop_vrh_1 as fensapice_drop_vrh_1_cls
from .fensapice_drop_vc import fensapice_drop_vc as fensapice_drop_vc_cls
class icing(Group):
    """
    Help not available.
    """

    fluent_name = "icing"

    child_names = \
        ['fensapice_flow_bc_subtype', 'fensapice_drop_bccustom',
         'fensapice_drop_lwc', 'fensapice_drop_dtemp', 'fensapice_drop_ddiam',
         'fensapice_drop_dv', 'fensapice_drop_dx', 'fensapice_drop_dy',
         'fensapice_drop_dz', 'fensapice_dpm_surface_injection',
         'fensapice_dpm_inj_nstream', 'fensapice_drop_icc',
         'fensapice_drop_ctemp', 'fensapice_drop_cmelt',
         'fensapice_drop_cdiam', 'fensapice_drop_cv', 'fensapice_drop_cx',
         'fensapice_drop_cy', 'fensapice_drop_cz', 'fensapice_drop_vrh',
         'fensapice_drop_vrh_1', 'fensapice_drop_vc']

    _child_classes = dict(
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        fensapice_drop_bccustom=fensapice_drop_bccustom_cls,
        fensapice_drop_lwc=fensapice_drop_lwc_cls,
        fensapice_drop_dtemp=fensapice_drop_dtemp_cls,
        fensapice_drop_ddiam=fensapice_drop_ddiam_cls,
        fensapice_drop_dv=fensapice_drop_dv_cls,
        fensapice_drop_dx=fensapice_drop_dx_cls,
        fensapice_drop_dy=fensapice_drop_dy_cls,
        fensapice_drop_dz=fensapice_drop_dz_cls,
        fensapice_dpm_surface_injection=fensapice_dpm_surface_injection_cls,
        fensapice_dpm_inj_nstream=fensapice_dpm_inj_nstream_cls,
        fensapice_drop_icc=fensapice_drop_icc_cls,
        fensapice_drop_ctemp=fensapice_drop_ctemp_cls,
        fensapice_drop_cmelt=fensapice_drop_cmelt_cls,
        fensapice_drop_cdiam=fensapice_drop_cdiam_cls,
        fensapice_drop_cv=fensapice_drop_cv_cls,
        fensapice_drop_cx=fensapice_drop_cx_cls,
        fensapice_drop_cy=fensapice_drop_cy_cls,
        fensapice_drop_cz=fensapice_drop_cz_cls,
        fensapice_drop_vrh=fensapice_drop_vrh_cls,
        fensapice_drop_vrh_1=fensapice_drop_vrh_1_cls,
        fensapice_drop_vc=fensapice_drop_vc_cls,
    )

