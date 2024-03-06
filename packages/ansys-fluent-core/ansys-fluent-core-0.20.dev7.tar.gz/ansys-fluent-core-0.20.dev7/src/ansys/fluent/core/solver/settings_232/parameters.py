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

from .iter_count import iter_count as iter_count_cls
from .solution_stabilization_persistence import solution_stabilization_persistence as solution_stabilization_persistence_cls
from .persistence_fixed_time_steps import persistence_fixed_time_steps as persistence_fixed_time_steps_cls
from .persistence_fixed_duration import persistence_fixed_duration as persistence_fixed_duration_cls
from .extrapolation_method import extrapolation_method as extrapolation_method_cls
class parameters(Group):
    """
    'parameters' child.
    """

    fluent_name = "parameters"

    child_names = \
        ['iter_count', 'solution_stabilization_persistence',
         'persistence_fixed_time_steps', 'persistence_fixed_duration',
         'extrapolation_method']

    _child_classes = dict(
        iter_count=iter_count_cls,
        solution_stabilization_persistence=solution_stabilization_persistence_cls,
        persistence_fixed_time_steps=persistence_fixed_time_steps_cls,
        persistence_fixed_duration=persistence_fixed_duration_cls,
        extrapolation_method=extrapolation_method_cls,
    )

