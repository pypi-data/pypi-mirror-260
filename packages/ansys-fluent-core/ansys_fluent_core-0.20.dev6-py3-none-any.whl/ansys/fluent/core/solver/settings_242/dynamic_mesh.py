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
from .auto_1 import auto as auto_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls
class dynamic_mesh(Group):
    """
    Use load balancing for dynamic mesh?.
    """

    fluent_name = "dynamic-mesh"

    child_names = \
        ['use', 'auto', 'threshold', 'interval']

    _child_classes = dict(
        use=use_cls,
        auto=auto_cls,
        threshold=threshold_cls,
        interval=interval_cls,
    )

