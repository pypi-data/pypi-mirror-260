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

from .general_3 import general as general_cls
from .reference_frame_2 import reference_frame as reference_frame_cls
from .mesh_motion import mesh_motion as mesh_motion_cls
from .solid_motion import solid_motion as solid_motion_cls
from .source_terms_2 import source_terms as source_terms_cls
from .fixed_values import fixed_values as fixed_values_cls
from .material_orientation import material_orientation as material_orientation_cls
from .disabled_1 import disabled as disabled_cls
from .internal import internal as internal_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['general', 'reference_frame', 'mesh_motion', 'solid_motion',
         'source_terms', 'fixed_values', 'material_orientation', 'disabled',
         'internal']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
        general=general_cls,
        reference_frame=reference_frame_cls,
        mesh_motion=mesh_motion_cls,
        solid_motion=solid_motion_cls,
        source_terms=source_terms_cls,
        fixed_values=fixed_values_cls,
        material_orientation=material_orientation_cls,
        disabled=disabled_cls,
        internal=internal_cls,
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

    _child_aliases = dict(
        material="general/material",
    )

