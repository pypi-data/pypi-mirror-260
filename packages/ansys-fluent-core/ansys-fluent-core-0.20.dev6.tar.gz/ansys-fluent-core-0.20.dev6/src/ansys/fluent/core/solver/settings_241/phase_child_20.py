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

from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .loss_coefficient import loss_coefficient as loss_coefficient_cls
from .hc import hc as hc_cls
from .t_1 import t as t_cls
from .heat_flux import heat_flux as heat_flux_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .strength import strength as strength_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'porous_jump_turb_wall_treatment', 'loss_coefficient', 'hc', 't',
         'heat_flux', 'discrete_phase_bc_type', 'dem_collision_partner',
         'reinj_inj', 'discrete_phase_bc_function', 'strength']

    _child_classes = dict(
        geom_disable=geom_disable_cls,
        geom_dir_spec=geom_dir_spec_cls,
        geom_dir_x=geom_dir_x_cls,
        geom_dir_y=geom_dir_y_cls,
        geom_dir_z=geom_dir_z_cls,
        geom_levels=geom_levels_cls,
        geom_bgthread=geom_bgthread_cls,
        porous_jump_turb_wall_treatment=porous_jump_turb_wall_treatment_cls,
        loss_coefficient=loss_coefficient_cls,
        hc=hc_cls,
        t=t_cls,
        heat_flux=heat_flux_cls,
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        strength=strength_cls,
    )

