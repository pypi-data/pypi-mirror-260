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

from .blending_factor_1 import blending_factor as blending_factor_cls
from .bin_count import bin_count as bin_count_cls
class pressure_outlet(Group):
    """
    Select pressure specification method on pressure-outlet boundaries.
    """

    fluent_name = "pressure-outlet"

    child_names = \
        ['blending_factor', 'bin_count']

    _child_classes = dict(
        blending_factor=blending_factor_cls,
        bin_count=bin_count_cls,
    )

