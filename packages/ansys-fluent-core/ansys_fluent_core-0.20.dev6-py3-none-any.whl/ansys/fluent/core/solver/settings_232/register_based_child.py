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

from .name_3 import name as name_cls
from .register import register as register_cls
from .frequency_2 import frequency as frequency_cls
from .active_1 import active as active_cls
from .verbosity_9 import verbosity as verbosity_cls
from .monitor_1 import monitor as monitor_cls
class register_based_child(Group):
    """
    'child_object_type' of register_based.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity', 'monitor']

    _child_classes = dict(
        name=name_cls,
        register=register_cls,
        frequency=frequency_cls,
        active=active_cls,
        verbosity=verbosity_cls,
        monitor=monitor_cls,
    )

