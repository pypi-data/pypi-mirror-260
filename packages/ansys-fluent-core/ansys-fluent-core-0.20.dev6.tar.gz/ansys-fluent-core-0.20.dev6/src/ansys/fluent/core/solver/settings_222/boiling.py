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

from .heat_flux_relaxation_factor import heat_flux_relaxation_factor as heat_flux_relaxation_factor_cls
from .show_expert_options import show_expert_options as show_expert_options_cls
from .two_resistance_boiling_framework import two_resistance_boiling_framework as two_resistance_boiling_framework_cls
class boiling(Group):
    """
    'boiling' child.
    """

    fluent_name = "boiling"

    child_names = \
        ['heat_flux_relaxation_factor', 'show_expert_options',
         'two_resistance_boiling_framework']

    _child_classes = dict(
        heat_flux_relaxation_factor=heat_flux_relaxation_factor_cls,
        show_expert_options=show_expert_options_cls,
        two_resistance_boiling_framework=two_resistance_boiling_framework_cls,
    )

