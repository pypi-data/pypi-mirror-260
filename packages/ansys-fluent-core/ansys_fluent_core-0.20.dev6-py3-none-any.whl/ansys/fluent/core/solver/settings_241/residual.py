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

from .equations_1 import equations as equations_cls
from .options_9 import options as options_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .reset import reset as reset_cls
from .renormalize import renormalize as renormalize_cls
from .plot_1 import plot as plot_cls
class residual(Group):
    """
    Enter the residual monitors menu.
    """

    fluent_name = "residual"

    child_names = \
        ['equations', 'options', 'axes', 'curves']

    command_names = \
        ['reset', 'renormalize', 'plot']

    _child_classes = dict(
        equations=equations_cls,
        options=options_cls,
        axes=axes_cls,
        curves=curves_cls,
        reset=reset_cls,
        renormalize=renormalize_cls,
        plot=plot_cls,
    )

