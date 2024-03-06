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

from .method_13 import method as method_cls
from .dissipation import dissipation as dissipation_cls
from .residual_minimization import residual_minimization as residual_minimization_cls
class current_scheme(Group):
    """
    Current adjoint stabilization scheme controls menu.
    """

    fluent_name = "current-scheme"

    child_names = \
        ['method', 'dissipation', 'residual_minimization']

    _child_classes = dict(
        method=method_cls,
        dissipation=dissipation_cls,
        residual_minimization=residual_minimization_cls,
    )

