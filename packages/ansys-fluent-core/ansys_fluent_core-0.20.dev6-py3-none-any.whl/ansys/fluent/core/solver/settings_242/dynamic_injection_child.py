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

from .acd import acd as acd_cls
from .cd import cd as cd_cls
from .direction_2 import direction as direction_cls
from .angle_1 import angle as angle_cls
class dynamic_injection_child(Group):
    """
    'child_object_type' of dynamic_injection.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['acd', 'cd', 'direction', 'angle']

    _child_classes = dict(
        acd=acd_cls,
        cd=cd_cls,
        direction=direction_cls,
        angle=angle_cls,
    )

