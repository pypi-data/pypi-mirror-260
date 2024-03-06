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

from .numbers import numbers as numbers_cls
from .rules import rules as rules_cls
from .log_scale_1 import log_scale as log_scale_cls
from .auto_scale_1 import auto_scale as auto_scale_cls
from .labels import labels as labels_cls
class axes(Group):
    """
    'axes' child.
    """

    fluent_name = "axes"

    child_names = \
        ['numbers', 'rules', 'log_scale', 'auto_scale', 'labels']

    _child_classes = dict(
        numbers=numbers_cls,
        rules=rules_cls,
        log_scale=log_scale_cls,
        auto_scale=auto_scale_cls,
        labels=labels_cls,
    )

