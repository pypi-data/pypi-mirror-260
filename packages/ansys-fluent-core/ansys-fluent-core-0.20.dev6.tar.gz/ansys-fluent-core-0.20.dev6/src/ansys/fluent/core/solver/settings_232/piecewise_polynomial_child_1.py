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

from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .coefficients_1 import coefficients as coefficients_cls
class piecewise_polynomial_child(Group):
    """
    'child_object_type' of piecewise_polynomial.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['minimum', 'maximum', 'number_of_coeff', 'coefficients']

    _child_classes = dict(
        minimum=minimum_cls,
        maximum=maximum_cls,
        number_of_coeff=number_of_coeff_cls,
        coefficients=coefficients_cls,
    )

