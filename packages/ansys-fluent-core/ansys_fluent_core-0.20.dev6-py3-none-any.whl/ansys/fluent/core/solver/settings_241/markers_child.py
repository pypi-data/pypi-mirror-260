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

from .symbol import symbol as symbol_cls
from .size import size as size_cls
from .color_1 import color as color_cls
class markers_child(Group):
    """
    'child_object_type' of markers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['symbol', 'size', 'color']

    _child_classes = dict(
        symbol=symbol_cls,
        size=size_cls,
        color=color_cls,
    )

