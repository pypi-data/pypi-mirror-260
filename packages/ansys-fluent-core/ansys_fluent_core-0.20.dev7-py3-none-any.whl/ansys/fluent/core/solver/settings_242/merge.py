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

from .merge_small_regions import merge_small_regions as merge_small_regions_cls
from .max_merge_iterations import max_merge_iterations as max_merge_iterations_cls
class merge(Group):
    """
    Set partition merging optimization.
    """

    fluent_name = "merge"

    child_names = \
        ['merge_small_regions', 'max_merge_iterations']

    _child_classes = dict(
        merge_small_regions=merge_small_regions_cls,
        max_merge_iterations=max_merge_iterations_cls,
    )

