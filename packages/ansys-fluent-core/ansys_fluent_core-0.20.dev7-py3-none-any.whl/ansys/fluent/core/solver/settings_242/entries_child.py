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

from .coefficient_3 import coefficient as coefficient_cls
from .observable import observable as observable_cls
from .power import power as power_cls
class entries_child(Group):
    """
    'child_object_type' of entries.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'observable', 'power']

    _child_classes = dict(
        coefficient=coefficient_cls,
        observable=observable_cls,
        power=power_cls,
    )

