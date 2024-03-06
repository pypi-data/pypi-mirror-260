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

from .compute_statistics import compute_statistics as compute_statistics_cls
from .statistics_level import statistics_level as statistics_level_cls
class miscellaneous(Group):
    """
    'miscellaneous' child.
    """

    fluent_name = "miscellaneous"

    child_names = \
        ['compute_statistics', 'statistics_level']

    _child_classes = dict(
        compute_statistics=compute_statistics_cls,
        statistics_level=statistics_level_cls,
    )

