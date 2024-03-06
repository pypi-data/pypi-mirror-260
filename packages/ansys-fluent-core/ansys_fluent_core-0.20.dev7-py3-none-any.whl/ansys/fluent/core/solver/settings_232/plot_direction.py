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

from .option import option as option_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .curve_length import curve_length as curve_length_cls
class plot_direction(Group):
    """
    'plot_direction' child.
    """

    fluent_name = "plot-direction"

    child_names = \
        ['option', 'direction_vector', 'curve_length']

    _child_classes = dict(
        option=option_cls,
        direction_vector=direction_vector_cls,
        curve_length=curve_length_cls,
    )

