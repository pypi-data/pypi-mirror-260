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

from .minimum import minimum as minimum_cls
from .maximum import maximum as maximum_cls
from .coefficients_2 import coefficients as coefficients_cls
class range_child(Group):
    """
    'child_object_type' of range.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['minimum', 'maximum', 'coefficients']

    _child_classes = dict(
        minimum=minimum_cls,
        maximum=maximum_cls,
        coefficients=coefficients_cls,
    )

