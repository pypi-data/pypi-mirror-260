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

from .enabled_11 import enabled as enabled_cls
from .always_use_face_centroid_with_periodics import always_use_face_centroid_with_periodics as always_use_face_centroid_with_periodics_cls
from .flow_interpolation import flow_interpolation as flow_interpolation_cls
from .boundary_layer_tracking_enabled import boundary_layer_tracking_enabled as boundary_layer_tracking_enabled_cls
from .subtet_validity_checking_enabled import subtet_validity_checking_enabled as subtet_validity_checking_enabled_cls
from .auto_intersect_tol_enabled import auto_intersect_tol_enabled as auto_intersect_tol_enabled_cls
from .barycentric_intersection_enabled import barycentric_intersection_enabled as barycentric_intersection_enabled_cls
from .particle_relocation import particle_relocation as particle_relocation_cls
from .stuck_particle_removal_enabled import stuck_particle_removal_enabled as stuck_particle_removal_enabled_cls
from .barycentric_sampling_enabled import barycentric_sampling_enabled as barycentric_sampling_enabled_cls
from .quad_face_centroid_enabled import quad_face_centroid_enabled as quad_face_centroid_enabled_cls
class high_res_tracking(Group):
    """
    Main menu containing settings that control the High-Res Tracking scheme.
    When the High-Res Tracking option is enabled (default), the computational cells are decomposed into tetrahedrons
    (subtets) and the particles tracked through the subtets. This option provides a more robust tracking
    algorithm and improved variable interpolation. If High-Res Tracking is not enabled, particles are tracked through
    the computational cells directly. Flow variables that appear in particle equations either use cell-center values
    or a truncated Taylor series approximation for interpolation to the particle position.
    """

    fluent_name = "high-res-tracking"

    child_names = \
        ['enabled', 'always_use_face_centroid_with_periodics',
         'flow_interpolation', 'boundary_layer_tracking_enabled',
         'subtet_validity_checking_enabled', 'auto_intersect_tol_enabled',
         'barycentric_intersection_enabled', 'particle_relocation',
         'stuck_particle_removal_enabled', 'barycentric_sampling_enabled',
         'quad_face_centroid_enabled']

    _child_classes = dict(
        enabled=enabled_cls,
        always_use_face_centroid_with_periodics=always_use_face_centroid_with_periodics_cls,
        flow_interpolation=flow_interpolation_cls,
        boundary_layer_tracking_enabled=boundary_layer_tracking_enabled_cls,
        subtet_validity_checking_enabled=subtet_validity_checking_enabled_cls,
        auto_intersect_tol_enabled=auto_intersect_tol_enabled_cls,
        barycentric_intersection_enabled=barycentric_intersection_enabled_cls,
        particle_relocation=particle_relocation_cls,
        stuck_particle_removal_enabled=stuck_particle_removal_enabled_cls,
        barycentric_sampling_enabled=barycentric_sampling_enabled_cls,
        quad_face_centroid_enabled=quad_face_centroid_enabled_cls,
    )

