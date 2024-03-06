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

from .method_11 import method as method_cls
from .type_2 import type as type_cls
from .interval_1 import interval as interval_cls
from .frequency_1 import frequency as frequency_cls
from .iteration import iteration as iteration_cls
class single_session_coupling(Group):
    """
    'single_session_coupling' child.
    """

    fluent_name = "single-session-coupling"

    child_names = \
        ['method', 'type', 'interval', 'frequency', 'iteration']

    _child_classes = dict(
        method=method_cls,
        type=type_cls,
        interval=interval_cls,
        frequency=frequency_cls,
        iteration=iteration_cls,
    )

