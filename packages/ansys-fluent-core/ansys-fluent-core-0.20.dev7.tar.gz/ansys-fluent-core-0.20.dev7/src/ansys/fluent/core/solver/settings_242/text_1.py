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

from .application import application as application_cls
from .border_3 import border as border_cls
from .bottom_3 import bottom as bottom_cls
from .clear_3 import clear as clear_cls
from .company import company as company_cls
from .date import date as date_cls
from .left_3 import left as left_cls
from .right_4 import right as right_cls
from .top_3 import top as top_cls
from .visible_5 import visible as visible_cls
from .alignment import alignment as alignment_cls
class text(Group):
    """
    Enter the text window options menu.
    """

    fluent_name = "text"

    child_names = \
        ['application', 'border', 'bottom', 'clear', 'company', 'date',
         'left', 'right', 'top', 'visible', 'alignment']

    _child_classes = dict(
        application=application_cls,
        border=border_cls,
        bottom=bottom_cls,
        clear=clear_cls,
        company=company_cls,
        date=date_cls,
        left=left_cls,
        right=right_cls,
        top=top_cls,
        visible=visible_cls,
        alignment=alignment_cls,
    )

