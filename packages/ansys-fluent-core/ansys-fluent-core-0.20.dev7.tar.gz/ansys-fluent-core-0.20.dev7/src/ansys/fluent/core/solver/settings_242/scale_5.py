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

from .border_2 import border as border_cls
from .bottom_2 import bottom as bottom_cls
from .clear_2 import clear as clear_cls
from .format_1 import format as format_cls
from .font_size_1 import font_size as font_size_cls
from .left_2 import left as left_cls
from .margin import margin as margin_cls
from .right_3 import right as right_cls
from .top_2 import top as top_cls
from .visible_4 import visible as visible_cls
class scale(Group):
    """
    Enter the color scale window options menu.
    """

    fluent_name = "scale"

    child_names = \
        ['border', 'bottom', 'clear', 'format', 'font_size', 'left', 'margin',
         'right', 'top', 'visible']

    _child_classes = dict(
        border=border_cls,
        bottom=bottom_cls,
        clear=clear_cls,
        format=format_cls,
        font_size=font_size_cls,
        left=left_cls,
        margin=margin_cls,
        right=right_cls,
        top=top_cls,
        visible=visible_cls,
    )

