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

from .settings_2 import settings as settings_cls
from .reset import reset as reset_cls
from .invert import invert as invert_cls
class transparency_options(Group):
    """
    'transparency_options' child.
    """

    fluent_name = "transparency-options"

    child_names = \
        ['settings', 'reset', 'invert']

    _child_classes = dict(
        settings=settings_cls,
        reset=reset_cls,
        invert=invert_cls,
    )

