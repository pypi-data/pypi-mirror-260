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

from .exponent_h2 import exponent_h2 as exponent_h2_cls
from .exponent_o2 import exponent_o2 as exponent_o2_cls
from .exponent_h2o import exponent_h2o as exponent_h2o_cls
class concentration_exp(Group):
    """
    Enter the concentration exponents settings.
    """

    fluent_name = "concentration-exp"

    child_names = \
        ['exponent_h2', 'exponent_o2', 'exponent_h2o']

    _child_classes = dict(
        exponent_h2=exponent_h2_cls,
        exponent_o2=exponent_o2_cls,
        exponent_h2o=exponent_h2o_cls,
    )

