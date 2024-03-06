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

from .high_order_pressure import high_order_pressure as high_order_pressure_cls
from .interpolation_method import interpolation_method as interpolation_method_cls
from .orphan_cell_treatment import orphan_cell_treatment as orphan_cell_treatment_cls
from .expert_2 import expert as expert_cls
class overset(Group):
    """
    Enter overset solver options menu.
    """

    fluent_name = "overset"

    child_names = \
        ['high_order_pressure', 'interpolation_method',
         'orphan_cell_treatment', 'expert']

    _child_classes = dict(
        high_order_pressure=high_order_pressure_cls,
        interpolation_method=interpolation_method_cls,
        orphan_cell_treatment=orphan_cell_treatment_cls,
        expert=expert_cls,
    )

