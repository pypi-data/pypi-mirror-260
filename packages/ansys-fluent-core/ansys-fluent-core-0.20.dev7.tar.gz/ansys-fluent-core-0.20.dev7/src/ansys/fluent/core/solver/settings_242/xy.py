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

from .border_4 import border as border_cls
from .bottom_4 import bottom as bottom_cls
from .left_4 import left as left_cls
from .right_5 import right as right_cls
from .top_4 import top as top_cls
from .visible_6 import visible as visible_cls
class xy(Group):
    """
    Enter the X-Y plot window options menu.
    """

    fluent_name = "xy"

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

