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

from .tolerance_3 import tolerance as tolerance_cls
from .max_iterations import max_iterations as max_iterations_cls
from .show_iterations import show_iterations as show_iterations_cls
class amg(Group):
    """
    Adjoint algebraic multigrid menu.
    """

    fluent_name = "amg"

    child_names = \
        ['tolerance', 'max_iterations', 'show_iterations']

    _child_classes = dict(
        tolerance=tolerance_cls,
        max_iterations=max_iterations_cls,
        show_iterations=show_iterations_cls,
    )

