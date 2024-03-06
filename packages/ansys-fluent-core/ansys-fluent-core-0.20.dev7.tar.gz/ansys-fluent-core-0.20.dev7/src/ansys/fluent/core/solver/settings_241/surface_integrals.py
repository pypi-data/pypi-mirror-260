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

from .area_1 import area as area_cls
from .area_weighted_avg import area_weighted_avg as area_weighted_avg_cls
from .vector_based_flux import vector_based_flux as vector_based_flux_cls
from .vector_flux import vector_flux as vector_flux_cls
from .vector_weighted_average import vector_weighted_average as vector_weighted_average_cls
from .facet_avg import facet_avg as facet_avg_cls
from .facet_min import facet_min as facet_min_cls
from .facet_max import facet_max as facet_max_cls
from .flow_rate_1 import flow_rate as flow_rate_cls
from .integral import integral as integral_cls
from .mass_flow_rate_4 import mass_flow_rate as mass_flow_rate_cls
from .mass_weighted_avg import mass_weighted_avg as mass_weighted_avg_cls
from .standard_deviation import standard_deviation as standard_deviation_cls
from .sum import sum as sum_cls
from .uniformity_index_area_weighted import uniformity_index_area_weighted as uniformity_index_area_weighted_cls
from .uniformity_index_mass_weighted import uniformity_index_mass_weighted as uniformity_index_mass_weighted_cls
from .vertex_avg import vertex_avg as vertex_avg_cls
from .vertex_min import vertex_min as vertex_min_cls
from .vertex_max import vertex_max as vertex_max_cls
from .volume_flow_rate import volume_flow_rate as volume_flow_rate_cls
class surface_integrals(Group):
    """
    'surface_integrals' child.
    """

    fluent_name = "surface-integrals"

    command_names = \
        ['area', 'area_weighted_avg', 'vector_based_flux', 'vector_flux',
         'vector_weighted_average', 'facet_avg', 'facet_min', 'facet_max',
         'flow_rate', 'integral', 'mass_flow_rate', 'mass_weighted_avg',
         'standard_deviation', 'sum', 'uniformity_index_area_weighted',
         'uniformity_index_mass_weighted', 'vertex_avg', 'vertex_min',
         'vertex_max', 'volume_flow_rate']

    _child_classes = dict(
        area=area_cls,
        area_weighted_avg=area_weighted_avg_cls,
        vector_based_flux=vector_based_flux_cls,
        vector_flux=vector_flux_cls,
        vector_weighted_average=vector_weighted_average_cls,
        facet_avg=facet_avg_cls,
        facet_min=facet_min_cls,
        facet_max=facet_max_cls,
        flow_rate=flow_rate_cls,
        integral=integral_cls,
        mass_flow_rate=mass_flow_rate_cls,
        mass_weighted_avg=mass_weighted_avg_cls,
        standard_deviation=standard_deviation_cls,
        sum=sum_cls,
        uniformity_index_area_weighted=uniformity_index_area_weighted_cls,
        uniformity_index_mass_weighted=uniformity_index_mass_weighted_cls,
        vertex_avg=vertex_avg_cls,
        vertex_min=vertex_min_cls,
        vertex_max=vertex_max_cls,
        volume_flow_rate=volume_flow_rate_cls,
    )

