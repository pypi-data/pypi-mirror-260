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

from .banded_coloring import banded_coloring as banded_coloring_cls
from .number_of_bands_1 import number_of_bands as number_of_bands_cls
class coloring(Group):
    """
    Select coloring option.
    """

    fluent_name = "coloring"

    child_names = \
        ['banded_coloring', 'number_of_bands']

    _child_classes = dict(
        banded_coloring=banded_coloring_cls,
        number_of_bands=number_of_bands_cls,
    )

