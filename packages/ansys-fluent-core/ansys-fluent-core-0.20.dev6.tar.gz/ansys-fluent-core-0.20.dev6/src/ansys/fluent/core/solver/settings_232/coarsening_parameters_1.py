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

from .max_coarse_levels_1 import max_coarse_levels as max_coarse_levels_cls
from .coarsen_by_interval_1 import coarsen_by_interval as coarsen_by_interval_cls
from .conservative_coarsening import conservative_coarsening as conservative_coarsening_cls
from .aggressive_coarsening_1 import aggressive_coarsening as aggressive_coarsening_cls
from .laplace_coarsening import laplace_coarsening as laplace_coarsening_cls
class coarsening_parameters(Group):
    """
    'coarsening_parameters' child.
    """

    fluent_name = "coarsening-parameters"

    child_names = \
        ['max_coarse_levels', 'coarsen_by_interval',
         'conservative_coarsening', 'aggressive_coarsening',
         'laplace_coarsening']

    _child_classes = dict(
        max_coarse_levels=max_coarse_levels_cls,
        coarsen_by_interval=coarsen_by_interval_cls,
        conservative_coarsening=conservative_coarsening_cls,
        aggressive_coarsening=aggressive_coarsening_cls,
        laplace_coarsening=laplace_coarsening_cls,
    )

