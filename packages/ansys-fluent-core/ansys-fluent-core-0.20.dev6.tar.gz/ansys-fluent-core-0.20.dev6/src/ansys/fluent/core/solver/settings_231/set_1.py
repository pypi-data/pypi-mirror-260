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

from .name_2 import name as name_cls
from .register import register as register_cls
from .frequency_2 import frequency as frequency_cls
from .active_1 import active as active_cls
from .verbosity_6 import verbosity as verbosity_cls
class set(Group):
    """
    Edit a definition for automatic poor mesh numerics.
    """

    fluent_name = "set"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity']

    _child_classes = dict(
        name=name_cls,
        register=register_cls,
        frequency=frequency_cls,
        active=active_cls,
        verbosity=verbosity_cls,
    )

