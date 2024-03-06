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

from .nfaces_as_weights import nfaces_as_weights as nfaces_as_weights_cls
from .user_defined_value import user_defined_value as user_defined_value_cls
from .value_1 import value as value_cls
class nfaces_as_weights(Group):
    """
    Use number of faces as weights.
    """

    fluent_name = "nfaces-as-weights"

    child_names = \
        ['nfaces_as_weights', 'user_defined_value', 'value']

    _child_classes = dict(
        nfaces_as_weights=nfaces_as_weights_cls,
        user_defined_value=user_defined_value_cls,
        value=value_cls,
    )

