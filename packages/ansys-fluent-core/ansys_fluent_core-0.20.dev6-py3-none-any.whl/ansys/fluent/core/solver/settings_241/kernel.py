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

from .option_4 import option as option_cls
from .gaussian_factor import gaussian_factor as gaussian_factor_cls
class kernel(Group):
    """
    'kernel' child.
    """

    fluent_name = "kernel"

    child_names = \
        ['option', 'gaussian_factor']

    _child_classes = dict(
        option=option_cls,
        gaussian_factor=gaussian_factor_cls,
    )

