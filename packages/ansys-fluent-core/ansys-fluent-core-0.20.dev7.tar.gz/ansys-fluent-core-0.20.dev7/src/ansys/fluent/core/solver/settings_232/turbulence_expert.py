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

from .low_re_ke import low_re_ke as low_re_ke_cls
from .low_re_ke_index import low_re_ke_index as low_re_ke_index_cls
from .kato_launder_model import kato_launder_model as kato_launder_model_cls
from .production_limiter import production_limiter as production_limiter_cls
from .kw_vorticity_based_production import kw_vorticity_based_production as kw_vorticity_based_production_cls
from .kw_add_sas import kw_add_sas as kw_add_sas_cls
from .kw_add_des import kw_add_des as kw_add_des_cls
from .turb_add_sbes_sdes import turb_add_sbes_sdes as turb_add_sbes_sdes_cls
from .sbes_sdes_hybrid_model import sbes_sdes_hybrid_model as sbes_sdes_hybrid_model_cls
from .sbes_update_interval_k_omega import sbes_update_interval_k_omega as sbes_update_interval_k_omega_cls
from .sbes_sgs_option import sbes_sgs_option as sbes_sgs_option_cls
from .sbes_les_subgrid_dynamic_fvar import sbes_les_subgrid_dynamic_fvar as sbes_les_subgrid_dynamic_fvar_cls
from .turbulence_damping import turbulence_damping as turbulence_damping_cls
from .rke_cmu_rotation_term import rke_cmu_rotation_term as rke_cmu_rotation_term_cls
from .turb_non_newtonian import turb_non_newtonian as turb_non_newtonian_cls
from .non_newtonian_modification import non_newtonian_modification as non_newtonian_modification_cls
from .turb_pk_compressible import turb_pk_compressible as turb_pk_compressible_cls
from .thermal_p_function import thermal_p_function as thermal_p_function_cls
from .restore_sst_v61 import restore_sst_v61 as restore_sst_v61_cls
class turbulence_expert(Group):
    """
    'turbulence_expert' child.
    """

    fluent_name = "turbulence-expert"

    child_names = \
        ['low_re_ke', 'low_re_ke_index', 'kato_launder_model',
         'production_limiter', 'kw_vorticity_based_production', 'kw_add_sas',
         'kw_add_des', 'turb_add_sbes_sdes', 'sbes_sdes_hybrid_model',
         'sbes_update_interval_k_omega', 'sbes_sgs_option',
         'sbes_les_subgrid_dynamic_fvar', 'turbulence_damping',
         'rke_cmu_rotation_term', 'turb_non_newtonian',
         'non_newtonian_modification', 'turb_pk_compressible',
         'thermal_p_function', 'restore_sst_v61']

    _child_classes = dict(
        low_re_ke=low_re_ke_cls,
        low_re_ke_index=low_re_ke_index_cls,
        kato_launder_model=kato_launder_model_cls,
        production_limiter=production_limiter_cls,
        kw_vorticity_based_production=kw_vorticity_based_production_cls,
        kw_add_sas=kw_add_sas_cls,
        kw_add_des=kw_add_des_cls,
        turb_add_sbes_sdes=turb_add_sbes_sdes_cls,
        sbes_sdes_hybrid_model=sbes_sdes_hybrid_model_cls,
        sbes_update_interval_k_omega=sbes_update_interval_k_omega_cls,
        sbes_sgs_option=sbes_sgs_option_cls,
        sbes_les_subgrid_dynamic_fvar=sbes_les_subgrid_dynamic_fvar_cls,
        turbulence_damping=turbulence_damping_cls,
        rke_cmu_rotation_term=rke_cmu_rotation_term_cls,
        turb_non_newtonian=turb_non_newtonian_cls,
        non_newtonian_modification=non_newtonian_modification_cls,
        turb_pk_compressible=turb_pk_compressible_cls,
        thermal_p_function=thermal_p_function_cls,
        restore_sst_v61=restore_sst_v61_cls,
    )

