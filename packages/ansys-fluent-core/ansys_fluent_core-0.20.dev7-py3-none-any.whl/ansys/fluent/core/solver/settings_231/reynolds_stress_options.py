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

from .solve_tke import solve_tke as solve_tke_cls
from .wall_echo import wall_echo as wall_echo_cls
class reynolds_stress_options(Group):
    """
    'reynolds_stress_options' child.
    """

    fluent_name = "reynolds-stress-options"

    child_names = \
        ['solve_tke', 'wall_echo']

    _child_classes = dict(
        solve_tke=solve_tke_cls,
        wall_echo=wall_echo_cls,
    )

