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

from .min_value import min_value as min_value_cls
from .max_value import max_value as max_value_cls
class clip_to_range(Group):
    """
    'clip_to_range' child.
    """

    fluent_name = "clip-to-range"

    child_names = \
        ['min_value', 'max_value']

    _child_classes = dict(
        min_value=min_value_cls,
        max_value=max_value_cls,
    )

