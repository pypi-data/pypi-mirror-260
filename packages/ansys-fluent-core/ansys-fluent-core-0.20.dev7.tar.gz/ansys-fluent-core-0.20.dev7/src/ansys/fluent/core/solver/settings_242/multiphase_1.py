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

from .mp_compressive_beta_max import mp_compressive_beta_max as mp_compressive_beta_max_cls
from .mp_boiling_zone import mp_boiling_zone as mp_boiling_zone_cls
from .numerical_beach import numerical_beach as numerical_beach_cls
from .beach_id import beach_id as beach_id_cls
from .beach_multi_dir import beach_multi_dir as beach_multi_dir_cls
from .beach_damp_type import beach_damp_type as beach_damp_type_cls
from .beach_inlet_bndr import beach_inlet_bndr as beach_inlet_bndr_cls
from .beach_fs_level import beach_fs_level as beach_fs_level_cls
from .beach_bottom_level import beach_bottom_level as beach_bottom_level_cls
from .beach_dir_ni import beach_dir_ni as beach_dir_ni_cls
from .beach_dir_nj import beach_dir_nj as beach_dir_nj_cls
from .beach_dir_nk import beach_dir_nk as beach_dir_nk_cls
from .beach_damp_len_spec import beach_damp_len_spec as beach_damp_len_spec_cls
from .beach_end_point import beach_end_point as beach_end_point_cls
from .beach_wave_len import beach_wave_len as beach_wave_len_cls
from .beach_len_factor import beach_len_factor as beach_len_factor_cls
from .beach_start_point import beach_start_point as beach_start_point_cls
from .beach_dir_list import beach_dir_list as beach_dir_list_cls
from .beach_damp_relative import beach_damp_relative as beach_damp_relative_cls
from .beach_damp_resist_lin import beach_damp_resist_lin as beach_damp_resist_lin_cls
from .beach_damp_resist import beach_damp_resist as beach_damp_resist_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['mp_compressive_beta_max', 'mp_boiling_zone', 'numerical_beach',
         'beach_id', 'beach_multi_dir', 'beach_damp_type', 'beach_inlet_bndr',
         'beach_fs_level', 'beach_bottom_level', 'beach_dir_ni',
         'beach_dir_nj', 'beach_dir_nk', 'beach_damp_len_spec',
         'beach_end_point', 'beach_wave_len', 'beach_len_factor',
         'beach_start_point', 'beach_dir_list', 'beach_damp_relative',
         'beach_damp_resist_lin', 'beach_damp_resist']

    _child_classes = dict(
        mp_compressive_beta_max=mp_compressive_beta_max_cls,
        mp_boiling_zone=mp_boiling_zone_cls,
        numerical_beach=numerical_beach_cls,
        beach_id=beach_id_cls,
        beach_multi_dir=beach_multi_dir_cls,
        beach_damp_type=beach_damp_type_cls,
        beach_inlet_bndr=beach_inlet_bndr_cls,
        beach_fs_level=beach_fs_level_cls,
        beach_bottom_level=beach_bottom_level_cls,
        beach_dir_ni=beach_dir_ni_cls,
        beach_dir_nj=beach_dir_nj_cls,
        beach_dir_nk=beach_dir_nk_cls,
        beach_damp_len_spec=beach_damp_len_spec_cls,
        beach_end_point=beach_end_point_cls,
        beach_wave_len=beach_wave_len_cls,
        beach_len_factor=beach_len_factor_cls,
        beach_start_point=beach_start_point_cls,
        beach_dir_list=beach_dir_list_cls,
        beach_damp_relative=beach_damp_relative_cls,
        beach_damp_resist_lin=beach_damp_resist_lin_cls,
        beach_damp_resist=beach_damp_resist_cls,
    )

