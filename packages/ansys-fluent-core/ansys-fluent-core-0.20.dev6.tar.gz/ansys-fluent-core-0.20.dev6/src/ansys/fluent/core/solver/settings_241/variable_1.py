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

from .size_by import size_by as size_by_cls
from .range import range as range_cls
class variable(Group):
    """
    'variable' child.
    """

    fluent_name = "variable"

    child_names = \
        ['size_by', 'range']

    _child_classes = dict(
        size_by=size_by_cls,
        range=range_cls,
    )

