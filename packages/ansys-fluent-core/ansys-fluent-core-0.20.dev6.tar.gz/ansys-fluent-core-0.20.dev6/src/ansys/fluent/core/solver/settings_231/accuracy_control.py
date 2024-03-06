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
from .max_number_of_refinements import max_number_of_refinements as max_number_of_refinements_cls
from .tolerance import tolerance as tolerance_cls
class accuracy_control(Group):
    """
    'accuracy_control' child.
    """

    fluent_name = "accuracy-control"

    child_names = \
        ['option', 'max_number_of_refinements', 'tolerance']

    _child_classes = dict(
        option=option_cls,
        max_number_of_refinements=max_number_of_refinements_cls,
        tolerance=tolerance_cls,
    )

