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

from .enabled_3 import enabled as enabled_cls
from .set_5 import set as set_cls
class conjugate_heat_transfer(Group):
    """
    'conjugate_heat_transfer' child.
    """

    fluent_name = "conjugate-heat-transfer"

    child_names = \
        ['enabled', 'set']

    _child_classes = dict(
        enabled=enabled_cls,
        set=set_cls,
    )

