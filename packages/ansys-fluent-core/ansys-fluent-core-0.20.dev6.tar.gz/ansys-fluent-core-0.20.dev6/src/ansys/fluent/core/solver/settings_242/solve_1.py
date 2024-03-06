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

from .iterate_1 import iterate as iterate_cls
from .dual_time_iterate_1 import dual_time_iterate as dual_time_iterate_cls
class solve(Group):
    """
    'solve' child.
    """

    fluent_name = "solve"

    command_names = \
        ['iterate', 'dual_time_iterate']

    _child_classes = dict(
        iterate=iterate_cls,
        dual_time_iterate=dual_time_iterate_cls,
    )

