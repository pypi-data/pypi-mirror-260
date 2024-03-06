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

from .phase_1 import phase as phase_cls
from .material import material as material_cls
from .sources import sources as sources_cls
from .source_terms import source_terms as source_terms_cls
from .fixed import fixed as fixed_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
from .fixes import fixes as fixes_cls
from .motion_spec import motion_spec as motion_spec_cls
from .relative_to_thread import relative_to_thread as relative_to_thread_cls
from .omega import omega as omega_cls
from .axis_origin_component import axis_origin_component as axis_origin_component_cls
from .axis_direction_component import axis_direction_component as axis_direction_component_cls
from .udf_zmotion_name import udf_zmotion_name as udf_zmotion_name_cls
from .mrf_motion import mrf_motion as mrf_motion_cls
from .mrf_relative_to_thread import mrf_relative_to_thread as mrf_relative_to_thread_cls
from .mrf_omega import mrf_omega as mrf_omega_cls
from .reference_frame_velocity_components import reference_frame_velocity_components as reference_frame_velocity_components_cls
from .reference_frame_axis_origin_components import reference_frame_axis_origin_components as reference_frame_axis_origin_components_cls
from .reference_frame_axis_direction_components import reference_frame_axis_direction_components as reference_frame_axis_direction_components_cls
from .mrf_udf_zmotion_name import mrf_udf_zmotion_name as mrf_udf_zmotion_name_cls
from .mgrid_enable_transient import mgrid_enable_transient as mgrid_enable_transient_cls
from .mgrid_motion import mgrid_motion as mgrid_motion_cls
from .mgrid_relative_to_thread import mgrid_relative_to_thread as mgrid_relative_to_thread_cls
from .mgrid_omega import mgrid_omega as mgrid_omega_cls
from .moving_mesh_velocity_components import moving_mesh_velocity_components as moving_mesh_velocity_components_cls
from .moving_mesh_axis_origin_components import moving_mesh_axis_origin_components as moving_mesh_axis_origin_components_cls
from .mgrid_udf_zmotion_name import mgrid_udf_zmotion_name as mgrid_udf_zmotion_name_cls
from .solid_motion import solid_motion as solid_motion_cls
from .solid_relative_to_thread import solid_relative_to_thread as solid_relative_to_thread_cls
from .solid_omega import solid_omega as solid_omega_cls
from .solid_motion_velocity_components import solid_motion_velocity_components as solid_motion_velocity_components_cls
from .solid_motion_axis_origin_components import solid_motion_axis_origin_components as solid_motion_axis_origin_components_cls
from .solid_motion_axis_direction_components import solid_motion_axis_direction_components as solid_motion_axis_direction_components_cls
from .solid_udf_zmotion_name import solid_udf_zmotion_name as solid_udf_zmotion_name_cls
from .radiating import radiating as radiating_cls
from .les_embedded import les_embedded as les_embedded_cls
from .contact_property import contact_property as contact_property_cls
from .vapor_phase_realgas import vapor_phase_realgas as vapor_phase_realgas_cls
from .cursys import cursys as cursys_cls
from .cursys_name import cursys_name as cursys_name_cls
from .pcb_model import pcb_model as pcb_model_cls
from .pcb_zone_info import pcb_zone_info as pcb_zone_info_cls
class solid_child(Group):
    """
    'child_object_type' of solid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'material', 'sources', 'source_terms', 'fixed',
         'cylindrical_fixed_var', 'fixes', 'motion_spec',
         'relative_to_thread', 'omega', 'axis_origin_component',
         'axis_direction_component', 'udf_zmotion_name', 'mrf_motion',
         'mrf_relative_to_thread', 'mrf_omega',
         'reference_frame_velocity_components',
         'reference_frame_axis_origin_components',
         'reference_frame_axis_direction_components', 'mrf_udf_zmotion_name',
         'mgrid_enable_transient', 'mgrid_motion', 'mgrid_relative_to_thread',
         'mgrid_omega', 'moving_mesh_velocity_components',
         'moving_mesh_axis_origin_components', 'mgrid_udf_zmotion_name',
         'solid_motion', 'solid_relative_to_thread', 'solid_omega',
         'solid_motion_velocity_components',
         'solid_motion_axis_origin_components',
         'solid_motion_axis_direction_components', 'solid_udf_zmotion_name',
         'radiating', 'les_embedded', 'contact_property',
         'vapor_phase_realgas', 'cursys', 'cursys_name', 'pcb_model',
         'pcb_zone_info']

    _child_classes = dict(
        phase=phase_cls,
        material=material_cls,
        sources=sources_cls,
        source_terms=source_terms_cls,
        fixed=fixed_cls,
        cylindrical_fixed_var=cylindrical_fixed_var_cls,
        fixes=fixes_cls,
        motion_spec=motion_spec_cls,
        relative_to_thread=relative_to_thread_cls,
        omega=omega_cls,
        axis_origin_component=axis_origin_component_cls,
        axis_direction_component=axis_direction_component_cls,
        udf_zmotion_name=udf_zmotion_name_cls,
        mrf_motion=mrf_motion_cls,
        mrf_relative_to_thread=mrf_relative_to_thread_cls,
        mrf_omega=mrf_omega_cls,
        reference_frame_velocity_components=reference_frame_velocity_components_cls,
        reference_frame_axis_origin_components=reference_frame_axis_origin_components_cls,
        reference_frame_axis_direction_components=reference_frame_axis_direction_components_cls,
        mrf_udf_zmotion_name=mrf_udf_zmotion_name_cls,
        mgrid_enable_transient=mgrid_enable_transient_cls,
        mgrid_motion=mgrid_motion_cls,
        mgrid_relative_to_thread=mgrid_relative_to_thread_cls,
        mgrid_omega=mgrid_omega_cls,
        moving_mesh_velocity_components=moving_mesh_velocity_components_cls,
        moving_mesh_axis_origin_components=moving_mesh_axis_origin_components_cls,
        mgrid_udf_zmotion_name=mgrid_udf_zmotion_name_cls,
        solid_motion=solid_motion_cls,
        solid_relative_to_thread=solid_relative_to_thread_cls,
        solid_omega=solid_omega_cls,
        solid_motion_velocity_components=solid_motion_velocity_components_cls,
        solid_motion_axis_origin_components=solid_motion_axis_origin_components_cls,
        solid_motion_axis_direction_components=solid_motion_axis_direction_components_cls,
        solid_udf_zmotion_name=solid_udf_zmotion_name_cls,
        radiating=radiating_cls,
        les_embedded=les_embedded_cls,
        contact_property=contact_property_cls,
        vapor_phase_realgas=vapor_phase_realgas_cls,
        cursys=cursys_cls,
        cursys_name=cursys_name_cls,
        pcb_model=pcb_model_cls,
        pcb_zone_info=pcb_zone_info_cls,
    )

