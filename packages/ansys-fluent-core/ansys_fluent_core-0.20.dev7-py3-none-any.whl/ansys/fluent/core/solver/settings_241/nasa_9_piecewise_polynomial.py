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

from .list_properties import list_properties as list_properties_cls
from .piecewise_polynomial_child import piecewise_polynomial_child

class nasa_9_piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    """
    Specify piecewise-polynomial settings.
    """

    fluent_name = "nasa-9-piecewise-polynomial"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: piecewise_polynomial_child = piecewise_polynomial_child
    """
    child_object_type of nasa_9_piecewise_polynomial.
    """
