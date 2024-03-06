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

from .two_stage_runge_kutta import two_stage_runge_kutta as two_stage_runge_kutta_cls
from .default_multi_stage_runge_kutta import default_multi_stage_runge_kutta as default_multi_stage_runge_kutta_cls
class rk2(Group):
    """
    'rk2' child.
    """

    fluent_name = "rk2"

    child_names = \
        ['two_stage_runge_kutta', 'default_multi_stage_runge_kutta']

    _child_classes = dict(
        two_stage_runge_kutta=two_stage_runge_kutta_cls,
        default_multi_stage_runge_kutta=default_multi_stage_runge_kutta_cls,
    )

