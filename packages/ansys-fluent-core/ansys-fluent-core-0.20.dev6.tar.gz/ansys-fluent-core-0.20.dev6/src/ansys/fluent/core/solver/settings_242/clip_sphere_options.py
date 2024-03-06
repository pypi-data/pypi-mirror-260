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
from .settings_5 import settings as settings_cls
from .reset import reset as reset_cls
class clip_sphere_options(Group):
    """
    'clip_sphere_options' child.
    """

    fluent_name = "clip-sphere-options"

    child_names = \
        ['selection_type', 'settings', 'reset']

    _child_classes = dict(
        selection_type=selection_type_cls,
        settings=settings_cls,
        reset=reset_cls,
    )

