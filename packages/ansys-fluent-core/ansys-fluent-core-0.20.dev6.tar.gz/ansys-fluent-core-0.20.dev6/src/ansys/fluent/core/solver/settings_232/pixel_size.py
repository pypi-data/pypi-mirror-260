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

from .width_1 import width as width_cls
from .height_1 import height as height_cls
from .margin_1 import margin as margin_cls
class pixel_size(Group):
    """
    'pixel_size' child.
    """

    fluent_name = "pixel-size"

    child_names = \
        ['width', 'height', 'margin']

    _child_classes = dict(
        width=width_cls,
        height=height_cls,
        margin=margin_cls,
    )

