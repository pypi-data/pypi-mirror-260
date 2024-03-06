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

from .active import active as active_cls
from .value_1 import value as value_cls
from .transparency import transparency as transparency_cls
from .color_2 import color as color_cls
class settings_child(Group):
    """
    'child_object_type' of settings.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['active', 'value', 'transparency', 'color']

    _child_classes = dict(
        active=active_cls,
        value=value_cls,
        transparency=transparency_cls,
        color=color_cls,
    )

