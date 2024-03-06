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

from .under_relaxation_factor import under_relaxation_factor as under_relaxation_factor_cls
from .verbosity_6 import verbosity as verbosity_cls
class target_mass_flow_rate_settings(Group):
    """
    Enter the targeted mass flow rate setting menu.
    """

    fluent_name = "target-mass-flow-rate-settings"

    child_names = \
        ['under_relaxation_factor', 'verbosity']

    _child_classes = dict(
        under_relaxation_factor=under_relaxation_factor_cls,
        verbosity=verbosity_cls,
    )

