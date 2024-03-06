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

from .border import border as border_cls
from .bottom import bottom as bottom_cls
from .clear_1 import clear as clear_cls
from .left import left as left_cls
from .right_1 import right as right_cls
from .top import top as top_cls
from .visible_2 import visible as visible_cls
class axes(Group):
    """
    Enter the axes window options menu.
    """

    fluent_name = "axes"

    child_names = \
        ['border', 'bottom', 'clear', 'left', 'right', 'top', 'visible']

    _child_classes = dict(
        border=border_cls,
        bottom=bottom_cls,
        clear=clear_cls,
        left=left_cls,
        right=right_cls,
        top=top_cls,
        visible=visible_cls,
    )

