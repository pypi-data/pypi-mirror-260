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

from .fixed_cycle_parameters_2 import fixed_cycle_parameters as fixed_cycle_parameters_cls
from .coarsening_parameters_2 import coarsening_parameters as coarsening_parameters_cls
from .relaxation_factor_2 import relaxation_factor as relaxation_factor_cls
from .options_8 import options as options_cls
class fas_mg_controls(Group):
    """
    Enter FAS multigrid controls menu.
    """

    fluent_name = "fas-mg-controls"

    child_names = \
        ['fixed_cycle_parameters', 'coarsening_parameters',
         'relaxation_factor', 'options']

    _child_classes = dict(
        fixed_cycle_parameters=fixed_cycle_parameters_cls,
        coarsening_parameters=coarsening_parameters_cls,
        relaxation_factor=relaxation_factor_cls,
        options=options_cls,
    )

