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

from .type_1 import type as type_cls
from .two_dim_space import two_dim_space as two_dim_space_cls
from .velocity_formulation import velocity_formulation as velocity_formulation_cls
from .time import time as time_cls
class solver(Group):
    """
    'solver' child.
    """

    fluent_name = "solver"

    child_names = \
        ['type', 'two_dim_space', 'velocity_formulation', 'time']

    _child_classes = dict(
        type=type_cls,
        two_dim_space=two_dim_space_cls,
        velocity_formulation=velocity_formulation_cls,
        time=time_cls,
    )

