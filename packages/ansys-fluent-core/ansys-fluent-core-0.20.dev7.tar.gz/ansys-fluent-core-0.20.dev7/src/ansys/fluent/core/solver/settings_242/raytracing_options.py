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

from .background_2 import background as background_cls
from .rendering import rendering as rendering_cls
from .display_live_preview import display_live_preview as display_live_preview_cls
class raytracing_options(Group):
    """
    'raytracing_options' child.
    """

    fluent_name = "raytracing-options"

    child_names = \
        ['background', 'rendering']

    command_names = \
        ['display_live_preview']

    _child_classes = dict(
        background=background_cls,
        rendering=rendering_cls,
        display_live_preview=display_live_preview_cls,
    )

