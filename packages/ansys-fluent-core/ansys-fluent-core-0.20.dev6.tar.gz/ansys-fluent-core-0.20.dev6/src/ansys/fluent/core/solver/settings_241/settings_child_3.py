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
from .x_center import x_center as x_center_cls
from .y_center import y_center as y_center_cls
from .z_center import z_center as z_center_cls
from .radius import radius as radius_cls
class settings_child(Group):
    """
    'child_object_type' of settings.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['active', 'x_center', 'y_center', 'z_center', 'radius']

    _child_classes = dict(
        active=active_cls,
        x_center=x_center_cls,
        y_center=y_center_cls,
        z_center=z_center_cls,
        radius=radius_cls,
    )

