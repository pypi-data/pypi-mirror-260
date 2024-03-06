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

from .adjoint_equations import adjoint_equations as adjoint_equations_cls
from .options_18 import options as options_cls
from .plot_1 import plot as plot_cls
class monitors(Group):
    """
    Enter the residual monitors menu.
    """

    fluent_name = "monitors"

    child_names = \
        ['adjoint_equations', 'options']

    command_names = \
        ['plot']

    _child_classes = dict(
        adjoint_equations=adjoint_equations_cls,
        options=options_cls,
        plot=plot_cls,
    )

