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

from .enabled_6 import enabled as enabled_cls
class pressure_gradient_force(Group):
    """
    'pressure_gradient_force' child.
    """

    fluent_name = "pressure-gradient-force"

    child_names = \
        ['enabled']

    _child_classes = dict(
        enabled=enabled_cls,
    )

