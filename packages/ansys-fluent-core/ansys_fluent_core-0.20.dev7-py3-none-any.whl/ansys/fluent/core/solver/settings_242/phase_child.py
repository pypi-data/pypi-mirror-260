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

from .zonal_models import zonal_models as zonal_models_cls
from .zonal_flow import zonal_flow as zonal_flow_cls
from .zonal_flow_spec import zonal_flow_spec as zonal_flow_spec_cls
from .general_2 import general as general_cls
from .conical import conical as conical_cls
from .reference_frame_1 import reference_frame as reference_frame_cls
from .mesh_motion import mesh_motion as mesh_motion_cls
from .porous_zone import porous_zone as porous_zone_cls
from .fan_zone_1 import fan_zone as fan_zone_cls
from .embedded_les import embedded_les as embedded_les_cls
from .reaction import reaction as reaction_cls
from .source_terms_2 import source_terms as source_terms_cls
from .fixed_values import fixed_values as fixed_values_cls
from .multiphase_1 import multiphase as multiphase_cls
from .disabled import disabled as disabled_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['zonal_models', 'zonal_flow', 'zonal_flow_spec', 'general',
         'conical', 'reference_frame', 'mesh_motion', 'porous_zone',
         'fan_zone', 'embedded_les', 'reaction', 'source_terms',
         'fixed_values', 'multiphase', 'disabled']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
        zonal_models=zonal_models_cls,
        zonal_flow=zonal_flow_cls,
        zonal_flow_spec=zonal_flow_spec_cls,
        general=general_cls,
        conical=conical_cls,
        reference_frame=reference_frame_cls,
        mesh_motion=mesh_motion_cls,
        porous_zone=porous_zone_cls,
        fan_zone=fan_zone_cls,
        embedded_les=embedded_les_cls,
        reaction=reaction_cls,
        source_terms=source_terms_cls,
        fixed_values=fixed_values_cls,
        multiphase=multiphase_cls,
        disabled=disabled_cls,
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

    _child_aliases = dict(
        material="general/material",
    )

