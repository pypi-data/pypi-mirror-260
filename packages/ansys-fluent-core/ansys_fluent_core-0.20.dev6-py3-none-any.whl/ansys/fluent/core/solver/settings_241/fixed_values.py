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

from .fixed import fixed as fixed_cls
from .fixes import fixes as fixes_cls
class fixed_values(Group):
    """
    Help not available.
    """

    fluent_name = "fixed-values"

    child_names = \
        ['fixed', 'fixes']

    _child_classes = dict(
        fixed=fixed_cls,
        fixes=fixes_cls,
    )

