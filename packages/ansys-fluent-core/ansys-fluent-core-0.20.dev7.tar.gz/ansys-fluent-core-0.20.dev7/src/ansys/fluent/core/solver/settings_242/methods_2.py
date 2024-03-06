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

from .discretization_1 import discretization as discretization_cls
from .default_1 import default as default_cls
from .balanced import balanced as balanced_cls
from .best_match import best_match as best_match_cls
class methods(Group):
    """
    Adjoint method or discretization menu.
    """

    fluent_name = "methods"

    child_names = \
        ['discretization']

    command_names = \
        ['default', 'balanced', 'best_match']

    _child_classes = dict(
        discretization=discretization_cls,
        default=default_cls,
        balanced=balanced_cls,
        best_match=best_match_cls,
    )

