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

from .data_type_4 import data_type as data_type_cls
from .value_6 import value as value_cls
from .profile_4 import profile as profile_cls
class tab_elec_current(Group):
    """
    Set electric current at terminal in FMU coupling method.
    """

    fluent_name = "tab-elec-current"

    child_names = \
        ['data_type', 'value', 'profile']

    _child_classes = dict(
        data_type=data_type_cls,
        value=value_cls,
        profile=profile_cls,
    )

