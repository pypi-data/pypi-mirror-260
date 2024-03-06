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

from .minimum_val import minimum_val as minimum_val_cls
from .maximum_val import maximum_val as maximum_val_cls
from .division_val import division_val as division_val_cls
class histogram_parameters(Group):
    """
    Enter the parameter menu for the histogram.
    """

    fluent_name = "histogram-parameters"

    child_names = \
        ['minimum_val', 'maximum_val', 'division_val']

    _child_classes = dict(
        minimum_val=minimum_val_cls,
        maximum_val=maximum_val_cls,
        division_val=division_val_cls,
    )

