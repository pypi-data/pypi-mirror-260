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

class method(String, _HasAllowedValuesMixin):
    """
    None: Solves adjoint equations with no stabilization.
    Dissipation: Introduces nonlinear damping in calculation domain.
    Residual Minimization: Uses Krylov subspace method to build a solution with minimum residual.
    """

    fluent_name = "method"

