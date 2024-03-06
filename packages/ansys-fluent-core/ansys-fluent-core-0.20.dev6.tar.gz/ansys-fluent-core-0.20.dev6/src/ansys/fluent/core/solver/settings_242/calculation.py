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

from .iteration_count import iteration_count as iteration_count_cls
from .initialize_stabilization import initialize_stabilization as initialize_stabilization_cls
from .calculation_activities import calculation_activities as calculation_activities_cls
from .initialize_2 import initialize as initialize_cls
from .calculate_1 import calculate as calculate_cls
class calculation(Group):
    """
    Enter the adjoint calculation menu.
    """

    fluent_name = "calculation"

    child_names = \
        ['iteration_count', 'initialize_stabilization',
         'calculation_activities']

    command_names = \
        ['initialize', 'calculate']

    _child_classes = dict(
        iteration_count=iteration_count_cls,
        initialize_stabilization=initialize_stabilization_cls,
        calculation_activities=calculation_activities_cls,
        initialize=initialize_cls,
        calculate=calculate_cls,
    )

