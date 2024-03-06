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

class strategy(String, _HasAllowedValuesMixin):
    """
    None: allows you to select a single stabilization method to be used throughout the calculation, or none at all.
    Blended: either no scheme (None) or the Dissipation scheme is applied at the beginning, then a second scheme (the Residual Minimization scheme) is used for the remainder of the calculation.
    """

    fluent_name = "strategy"

