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

from .type_2 import type as type_cls
from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls
class range_options(Group):
    """
    'range_options' child.
    """

    fluent_name = "range-options"

    child_names = \
        ['type', 'minimum', 'maximum']

    _child_classes = dict(
        type=type_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
    )

