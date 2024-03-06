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

from .rich_equivalence_ratio_limit import rich_equivalence_ratio_limit as rich_equivalence_ratio_limit_cls
from .exponential_factor_beta import exponential_factor_beta as exponential_factor_beta_cls
class equilibrium_rich_flammability_options(Group):
    """
    'equilibrium_rich_flammability_options' child.
    """

    fluent_name = "equilibrium-rich-flammability-options"

    child_names = \
        ['rich_equivalence_ratio_limit', 'exponential_factor_beta']

    _child_classes = dict(
        rich_equivalence_ratio_limit=rich_equivalence_ratio_limit_cls,
        exponential_factor_beta=exponential_factor_beta_cls,
    )

