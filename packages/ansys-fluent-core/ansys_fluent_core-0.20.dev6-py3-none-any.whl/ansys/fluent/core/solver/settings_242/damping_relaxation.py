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

class damping_relaxation(Real):
    """
    The damping relaxation can be used to control the rate at which the dissipation is updated as the adjoint solution progresses. As you decrease the value from 1, the rate at which the dissipation is updated is decreased.
    """

    fluent_name = "damping-relaxation"

