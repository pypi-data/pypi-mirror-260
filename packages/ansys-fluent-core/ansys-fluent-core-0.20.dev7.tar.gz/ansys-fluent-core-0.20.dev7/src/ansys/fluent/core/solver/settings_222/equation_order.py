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

from .solve_flow_last import solve_flow_last as solve_flow_last_cls
from .solve_exp_vof_at_end import solve_exp_vof_at_end as solve_exp_vof_at_end_cls
class equation_order(Group):
    """
    'equation_order' child.
    """

    fluent_name = "equation-order"

    child_names = \
        ['solve_flow_last', 'solve_exp_vof_at_end']

    _child_classes = dict(
        solve_flow_last=solve_flow_last_cls,
        solve_exp_vof_at_end=solve_exp_vof_at_end_cls,
    )

