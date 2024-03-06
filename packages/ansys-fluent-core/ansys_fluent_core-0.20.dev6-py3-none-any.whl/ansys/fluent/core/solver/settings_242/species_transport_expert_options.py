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

from .linearize_convection_source import linearize_convection_source as linearize_convection_source_cls
from .linearize_diffusion_source import linearize_diffusion_source as linearize_diffusion_source_cls
from .blending import blending as blending_cls
from .minimum_cell_quality_threshold import minimum_cell_quality_threshold as minimum_cell_quality_threshold_cls
class species_transport_expert_options(Group):
    """
    'species_transport_expert_options' child.
    """

    fluent_name = "species-transport-expert-options"

    child_names = \
        ['linearize_convection_source', 'linearize_diffusion_source',
         'blending', 'minimum_cell_quality_threshold']

    _child_classes = dict(
        linearize_convection_source=linearize_convection_source_cls,
        linearize_diffusion_source=linearize_diffusion_source_cls,
        blending=blending_cls,
        minimum_cell_quality_threshold=minimum_cell_quality_threshold_cls,
    )

