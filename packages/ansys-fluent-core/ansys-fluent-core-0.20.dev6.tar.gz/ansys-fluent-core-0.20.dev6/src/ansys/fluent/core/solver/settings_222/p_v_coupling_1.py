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

from .flow_scheme import flow_scheme as flow_scheme_cls
from .coupled_form import coupled_form as coupled_form_cls
from .solve_n_phase import solve_n_phase as solve_n_phase_cls
class p_v_coupling(Group):
    """
    'p_v_coupling' child.
    """

    fluent_name = "p-v-coupling"

    child_names = \
        ['flow_scheme', 'coupled_form', 'solve_n_phase']

    _child_classes = dict(
        flow_scheme=flow_scheme_cls,
        coupled_form=coupled_form_cls,
        solve_n_phase=solve_n_phase_cls,
    )

