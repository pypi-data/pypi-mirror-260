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

from .number_of_coefficients import number_of_coefficients as number_of_coefficients_cls
from .coefficients_1 import coefficients as coefficients_cls
class polynomial(Group):
    """
    Define a polynomial data profile.
    """

    fluent_name = "polynomial"

    child_names = \
        ['number_of_coefficients', 'coefficients']

    _child_classes = dict(
        number_of_coefficients=number_of_coefficients_cls,
        coefficients=coefficients_cls,
    )

