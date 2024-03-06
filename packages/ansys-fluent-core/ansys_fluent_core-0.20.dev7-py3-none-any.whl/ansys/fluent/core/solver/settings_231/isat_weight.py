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

from .use import use as use_cls
from .user_defined_2 import user_defined as user_defined_cls
from .value import value as value_cls
class isat_weight(Group):
    """
    Set ISAT weight.
    """

    fluent_name = "isat-weight"

    child_names = \
        ['use', 'user_defined', 'value']

    _child_classes = dict(
        use=use_cls,
        user_defined=user_defined_cls,
        value=value_cls,
    )

