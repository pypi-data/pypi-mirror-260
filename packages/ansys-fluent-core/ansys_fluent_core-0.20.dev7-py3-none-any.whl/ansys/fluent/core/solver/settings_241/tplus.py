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

from .method_4 import method as method_cls
from .value_1 import value as value_cls
from .user_defined import user_defined as user_defined_cls
class tplus(Group):
    """
    'tplus' child.
    """

    fluent_name = "tplus"

    child_names = \
        ['method', 'value', 'user_defined']

    _child_classes = dict(
        method=method_cls,
        value=value_cls,
        user_defined=user_defined_cls,
    )

