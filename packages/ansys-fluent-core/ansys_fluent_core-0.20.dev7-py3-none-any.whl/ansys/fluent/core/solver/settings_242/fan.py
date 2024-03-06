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

from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .dir import dir as dir_cls
from .average_dp import average_dp as average_dp_cls
from .pressure_jump import pressure_jump as pressure_jump_cls
from .limit_range import limit_range as limit_range_cls
from .v_min import v_min as v_min_cls
from .v_max import v_max as v_max_cls
from .strength import strength as strength_cls
from .profile_dp import profile_dp as profile_dp_cls
from .dp_profile import dp_profile as dp_profile_cls
from .swirl_model import swirl_model as swirl_model_cls
from .fan_vr import fan_vr as fan_vr_cls
from .fr import fr as fr_cls
from .hub import hub as hub_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .profile_vt import profile_vt as profile_vt_cls
from .vt_profile import vt_profile as vt_profile_cls
from .profile_vr import profile_vr as profile_vr_cls
from .vr_profile import vr_profile as vr_profile_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls
class fan(Group):
    """
    Help not available.
    """

    fluent_name = "fan"

    child_names = \
        ['porous_jump_turb_wall_treatment', 'dir', 'average_dp',
         'pressure_jump', 'limit_range', 'v_min', 'v_max', 'strength',
         'profile_dp', 'dp_profile', 'swirl_model', 'fan_vr', 'fr', 'hub',
         'axis_origin', 'axis_direction', 'profile_vt', 'vt_profile',
         'profile_vr', 'vr_profile', 'swirl_factor', 'discrete_phase_bc_type',
         'dem_collision_partner', 'reinj_inj', 'discrete_phase_bc_function',
         'new_fan_definition']

    _child_classes = dict(
        porous_jump_turb_wall_treatment=porous_jump_turb_wall_treatment_cls,
        dir=dir_cls,
        average_dp=average_dp_cls,
        pressure_jump=pressure_jump_cls,
        limit_range=limit_range_cls,
        v_min=v_min_cls,
        v_max=v_max_cls,
        strength=strength_cls,
        profile_dp=profile_dp_cls,
        dp_profile=dp_profile_cls,
        swirl_model=swirl_model_cls,
        fan_vr=fan_vr_cls,
        fr=fr_cls,
        hub=hub_cls,
        axis_origin=axis_origin_cls,
        axis_direction=axis_direction_cls,
        profile_vt=profile_vt_cls,
        vt_profile=vt_profile_cls,
        profile_vr=profile_vr_cls,
        vr_profile=vr_profile_cls,
        swirl_factor=swirl_factor_cls,
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        new_fan_definition=new_fan_definition_cls,
    )

