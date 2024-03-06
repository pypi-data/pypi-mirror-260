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

from .selection_type import selection_type as selection_type_cls
from .settings_4 import settings as settings_cls
from .reset_1 import reset as reset_cls
class clip_box_options(Group):
    """
    'clip_box_options' child.
    """

    fluent_name = "clip-box-options"

    child_names = \
        ['selection_type', 'settings']

    command_names = \
        ['reset']

    _child_classes = dict(
        selection_type=selection_type_cls,
        settings=settings_cls,
        reset=reset_cls,
    )

