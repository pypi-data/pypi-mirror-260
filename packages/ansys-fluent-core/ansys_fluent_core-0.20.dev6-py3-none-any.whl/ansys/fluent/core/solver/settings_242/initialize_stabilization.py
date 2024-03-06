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

from .strategy_1 import strategy as strategy_cls
from .scheme_2 import scheme as scheme_cls
class initialize_stabilization(Group):
    """
    Enter the stabilization initialization menu.
    """

    fluent_name = "initialize-stabilization"

    command_names = \
        ['strategy', 'scheme']

    _child_classes = dict(
        strategy=strategy_cls,
        scheme=scheme_cls,
    )

