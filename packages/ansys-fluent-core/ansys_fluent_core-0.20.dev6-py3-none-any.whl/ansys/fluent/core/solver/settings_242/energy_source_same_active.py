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

from .data_type_2 import data_type as data_type_cls
from .value_3 import value as value_cls
from .profile_1 import profile as profile_cls
class energy_source_same_active(Group):
    """
    Set same energy source for all zones.
    """

    fluent_name = "energy-source-same-active"

    child_names = \
        ['data_type', 'value', 'profile']

    _child_classes = dict(
        data_type=data_type_cls,
        value=value_cls,
        profile=profile_cls,
    )

