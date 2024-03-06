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

from .scalar_parameters import scalar_parameters as scalar_parameters_cls
from .coupled_parameters import coupled_parameters as coupled_parameters_cls
from .flexible_cycle_parameters import flexible_cycle_parameters as flexible_cycle_parameters_cls
from .options_7 import options as options_cls
class amg_controls(Group):
    """
    Enter AMG controls menu.
    """

    fluent_name = "amg-controls"

    child_names = \
        ['scalar_parameters', 'coupled_parameters',
         'flexible_cycle_parameters', 'options']

    _child_classes = dict(
        scalar_parameters=scalar_parameters_cls,
        coupled_parameters=coupled_parameters_cls,
        flexible_cycle_parameters=flexible_cycle_parameters_cls,
        options=options_cls,
    )

