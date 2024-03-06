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

from .growth_ratio import growth_ratio as growth_ratio_cls
class growth_ratio_refinement(Group):
    """
    'growth_ratio_refinement' child.
    """

    fluent_name = "growth-ratio-refinement"

    child_names = \
        ['growth_ratio']

    _child_classes = dict(
        growth_ratio=growth_ratio_cls,
    )

