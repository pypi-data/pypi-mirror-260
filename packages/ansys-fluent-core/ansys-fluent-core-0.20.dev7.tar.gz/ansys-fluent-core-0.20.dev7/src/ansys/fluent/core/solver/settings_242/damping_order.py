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

class damping_order(Integer):
    """
    The spatial order of the dissipation. A higher order leads to more intense and localized damping. This can typically be set to be one order larger than the adjoint calculation spatial order.
    """

    fluent_name = "damping-order"

