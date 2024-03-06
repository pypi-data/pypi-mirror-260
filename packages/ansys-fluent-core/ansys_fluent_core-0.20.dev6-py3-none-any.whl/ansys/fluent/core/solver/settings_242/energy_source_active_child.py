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

from .method_5 import method as method_cls
from .value_4 import value as value_cls
from .profile_2 import profile as profile_cls
class energy_source_active_child(Group):
    """
    'child_object_type' of energy_source_active.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['method', 'value', 'profile']

    _child_classes = dict(
        method=method_cls,
        value=value_cls,
        profile=profile_cls,
    )

