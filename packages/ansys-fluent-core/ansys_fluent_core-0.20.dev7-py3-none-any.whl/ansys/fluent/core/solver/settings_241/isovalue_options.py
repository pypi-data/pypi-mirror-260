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

from .hide_volume import hide_volume as hide_volume_cls
from .settings_3 import settings as settings_cls
from .reset_1 import reset as reset_cls
class isovalue_options(Group):
    """
    'isovalue_options' child.
    """

    fluent_name = "isovalue-options"

    child_names = \
        ['hide_volume', 'settings']

    command_names = \
        ['reset']

    _child_classes = dict(
        hide_volume=hide_volume_cls,
        settings=settings_cls,
        reset=reset_cls,
    )

