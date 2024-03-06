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

from .linearization import linearization as linearization_cls
from .implicit_momentum_coupling import implicit_momentum_coupling as implicit_momentum_coupling_cls
from .implicit_source_term_coupling import implicit_source_term_coupling as implicit_source_term_coupling_cls
from .linear_growth_of_dpm_source_terms import linear_growth_of_dpm_source_terms as linear_growth_of_dpm_source_terms_cls
from .reset_sources_at_timestep import reset_sources_at_timestep as reset_sources_at_timestep_cls
from .underrelaxation_factor import underrelaxation_factor as underrelaxation_factor_cls
from .second_order_time_accurate_sources_enabled import second_order_time_accurate_sources_enabled as second_order_time_accurate_sources_enabled_cls
class source_terms(Group):
    """
    'source_terms' child.
    """

    fluent_name = "source-terms"

    child_names = \
        ['linearization', 'implicit_momentum_coupling',
         'implicit_source_term_coupling', 'linear_growth_of_dpm_source_terms',
         'reset_sources_at_timestep', 'underrelaxation_factor',
         'second_order_time_accurate_sources_enabled']

    _child_classes = dict(
        linearization=linearization_cls,
        implicit_momentum_coupling=implicit_momentum_coupling_cls,
        implicit_source_term_coupling=implicit_source_term_coupling_cls,
        linear_growth_of_dpm_source_terms=linear_growth_of_dpm_source_terms_cls,
        reset_sources_at_timestep=reset_sources_at_timestep_cls,
        underrelaxation_factor=underrelaxation_factor_cls,
        second_order_time_accurate_sources_enabled=second_order_time_accurate_sources_enabled_cls,
    )

