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
from .x_min import x_min as x_min_cls
from .y_min import y_min as y_min_cls
from .z_min import z_min as z_min_cls
from .x_max import x_max as x_max_cls
from .y_max import y_max as y_max_cls
from .z_max import z_max as z_max_cls
class settings_child(Group):
    """
    'child_object_type' of settings.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['active', 'x_min', 'y_min', 'z_min', 'x_max', 'y_max', 'z_max']

    _child_classes = dict(
        active=active_cls,
        x_min=x_min_cls,
        y_min=y_min_cls,
        z_min=z_min_cls,
        x_max=x_max_cls,
        y_max=y_max_cls,
        z_max=z_max_cls,
    )

