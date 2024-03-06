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

from .adaption_method import adaption_method as adaption_method_cls
from .prismatic_boundary_zones import prismatic_boundary_zones as prismatic_boundary_zones_cls
from .cell_zones_1 import cell_zones as cell_zones_cls
from .dynamic_adaption_frequency import dynamic_adaption_frequency as dynamic_adaption_frequency_cls
from .verbosity import verbosity as verbosity_cls
from .encapsulate_children import encapsulate_children as encapsulate_children_cls
from .maximum_refinement_level import maximum_refinement_level as maximum_refinement_level_cls
from .minimum_edge_length import minimum_edge_length as minimum_edge_length_cls
from .minimum_cell_quality import minimum_cell_quality as minimum_cell_quality_cls
from .maximum_cell_count import maximum_cell_count as maximum_cell_count_cls
from .additional_refinement_layers import additional_refinement_layers as additional_refinement_layers_cls
from .prismatic_adaption import prismatic_adaption as prismatic_adaption_cls
from .prismatic_split_ratio import prismatic_split_ratio as prismatic_split_ratio_cls
from .overset_adapt_dead_cells import overset_adapt_dead_cells as overset_adapt_dead_cells_cls
from .dynamic_adaption import dynamic_adaption as dynamic_adaption_cls
class set(Group):
    """
    Enter the adaption set menu.
    """

    fluent_name = "set"

    child_names = \
        ['adaption_method', 'prismatic_boundary_zones', 'cell_zones',
         'dynamic_adaption_frequency', 'verbosity', 'encapsulate_children',
         'maximum_refinement_level', 'minimum_edge_length',
         'minimum_cell_quality', 'maximum_cell_count',
         'additional_refinement_layers', 'prismatic_adaption',
         'prismatic_split_ratio', 'overset_adapt_dead_cells']

    command_names = \
        ['dynamic_adaption']

    _child_classes = dict(
        adaption_method=adaption_method_cls,
        prismatic_boundary_zones=prismatic_boundary_zones_cls,
        cell_zones=cell_zones_cls,
        dynamic_adaption_frequency=dynamic_adaption_frequency_cls,
        verbosity=verbosity_cls,
        encapsulate_children=encapsulate_children_cls,
        maximum_refinement_level=maximum_refinement_level_cls,
        minimum_edge_length=minimum_edge_length_cls,
        minimum_cell_quality=minimum_cell_quality_cls,
        maximum_cell_count=maximum_cell_count_cls,
        additional_refinement_layers=additional_refinement_layers_cls,
        prismatic_adaption=prismatic_adaption_cls,
        prismatic_split_ratio=prismatic_split_ratio_cls,
        overset_adapt_dead_cells=overset_adapt_dead_cells_cls,
        dynamic_adaption=dynamic_adaption_cls,
    )

