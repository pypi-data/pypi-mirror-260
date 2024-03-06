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

from .equation_for_residual import equation_for_residual as equation_for_residual_cls
from .threshold import threshold as threshold_cls
class residual(Group):
    """
    'residual' child.
    """

    fluent_name = "residual"

    child_names = \
        ['equation_for_residual', 'threshold']

    _child_classes = dict(
        equation_for_residual=equation_for_residual_cls,
        threshold=threshold_cls,
    )

