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

from .scheme import scheme as scheme_cls
from .low_order_scheme import low_order_scheme as low_order_scheme_cls
from .high_order_scheme import high_order_scheme as high_order_scheme_cls
from .accuracy_control import accuracy_control as accuracy_control_cls
class tracking(Group):
    """
    'tracking' child.
    """

    fluent_name = "tracking"

    child_names = \
        ['scheme', 'low_order_scheme', 'high_order_scheme',
         'accuracy_control']

    _child_classes = dict(
        scheme=scheme_cls,
        low_order_scheme=low_order_scheme_cls,
        high_order_scheme=high_order_scheme_cls,
        accuracy_control=accuracy_control_cls,
    )

