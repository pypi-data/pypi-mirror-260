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

from .border_1 import border as border_cls
from .bottom_1 import bottom as bottom_cls
from .left_1 import left as left_cls
from .right_2 import right as right_cls
from .top_1 import top as top_cls
from .visible_3 import visible as visible_cls
class main(Group):
    """
    Enter the main view window options menu.
    """

    fluent_name = "main"

    child_names = \
        ['border', 'bottom', 'left', 'right', 'top', 'visible']

    _child_classes = dict(
        border=border_cls,
        bottom=bottom_cls,
        left=left_cls,
        right=right_cls,
        top=top_cls,
        visible=visible_cls,
    )

