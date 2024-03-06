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
from .use_user_define_value import use_user_define_value as use_user_define_value_cls
from .value import value as value_cls
class solid_thread_weight(Group):
    """
    Use solid thread weights.
    """

    fluent_name = "solid-thread-weight"

    child_names = \
        ['use', 'use_user_define_value', 'value']

    _child_classes = dict(
        use=use_cls,
        use_user_define_value=use_user_define_value_cls,
        value=value_cls,
    )

