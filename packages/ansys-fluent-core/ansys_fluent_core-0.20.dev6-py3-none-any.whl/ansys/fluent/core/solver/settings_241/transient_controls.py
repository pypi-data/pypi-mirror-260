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

from .type_9 import type as type_cls
from .method_9 import method as method_cls
from .duration_specification_method import duration_specification_method as duration_specification_method_cls
from .specified_time_step import specified_time_step as specified_time_step_cls
from .incremental_time import incremental_time as incremental_time_cls
from .time_step_count_2 import time_step_count as time_step_count_cls
from .total_time import total_time as total_time_cls
from .time_step_size import time_step_size as time_step_size_cls
from .max_iter_per_time_step import max_iter_per_time_step as max_iter_per_time_step_cls
from .total_time_step_count import total_time_step_count as total_time_step_count_cls
from .solution_status import solution_status as solution_status_cls
from .extrapolate_variables import extrapolate_variables as extrapolate_variables_cls
from .max_flow_time import max_flow_time as max_flow_time_cls
from .cfl_based_time_stepping import cfl_based_time_stepping as cfl_based_time_stepping_cls
from .cfl_based_time_stepping_advanced_options import cfl_based_time_stepping_advanced_options as cfl_based_time_stepping_advanced_options_cls
from .error_based_time_stepping import error_based_time_stepping as error_based_time_stepping_cls
from .undo_timestep import undo_timestep as undo_timestep_cls
from .predict_next import predict_next as predict_next_cls
from .rotating_mesh_flow_predictor import rotating_mesh_flow_predictor as rotating_mesh_flow_predictor_cls
from .mp_specific_time_stepping import mp_specific_time_stepping as mp_specific_time_stepping_cls
from .udf_hook import udf_hook as udf_hook_cls
from .fixed_periodic import fixed_periodic as fixed_periodic_cls
from .multiphase_specific_time_constraints import multiphase_specific_time_constraints as multiphase_specific_time_constraints_cls
from .solid_time_step_size import solid_time_step_size as solid_time_step_size_cls
from .time_step_size_for_acoustic_export import time_step_size_for_acoustic_export as time_step_size_for_acoustic_export_cls
from .extrapolate_eqn_vars import extrapolate_eqn_vars as extrapolate_eqn_vars_cls
class transient_controls(Group):
    """
    Enter transient controls menu.
    """

    fluent_name = "transient-controls"

    child_names = \
        ['type', 'method', 'duration_specification_method',
         'specified_time_step', 'incremental_time', 'time_step_count',
         'total_time', 'time_step_size', 'max_iter_per_time_step',
         'total_time_step_count', 'solution_status', 'extrapolate_variables',
         'max_flow_time', 'cfl_based_time_stepping',
         'cfl_based_time_stepping_advanced_options',
         'error_based_time_stepping', 'undo_timestep', 'predict_next',
         'rotating_mesh_flow_predictor', 'mp_specific_time_stepping',
         'udf_hook', 'fixed_periodic', 'multiphase_specific_time_constraints',
         'solid_time_step_size', 'time_step_size_for_acoustic_export',
         'extrapolate_eqn_vars']

    _child_classes = dict(
        type=type_cls,
        method=method_cls,
        duration_specification_method=duration_specification_method_cls,
        specified_time_step=specified_time_step_cls,
        incremental_time=incremental_time_cls,
        time_step_count=time_step_count_cls,
        total_time=total_time_cls,
        time_step_size=time_step_size_cls,
        max_iter_per_time_step=max_iter_per_time_step_cls,
        total_time_step_count=total_time_step_count_cls,
        solution_status=solution_status_cls,
        extrapolate_variables=extrapolate_variables_cls,
        max_flow_time=max_flow_time_cls,
        cfl_based_time_stepping=cfl_based_time_stepping_cls,
        cfl_based_time_stepping_advanced_options=cfl_based_time_stepping_advanced_options_cls,
        error_based_time_stepping=error_based_time_stepping_cls,
        undo_timestep=undo_timestep_cls,
        predict_next=predict_next_cls,
        rotating_mesh_flow_predictor=rotating_mesh_flow_predictor_cls,
        mp_specific_time_stepping=mp_specific_time_stepping_cls,
        udf_hook=udf_hook_cls,
        fixed_periodic=fixed_periodic_cls,
        multiphase_specific_time_constraints=multiphase_specific_time_constraints_cls,
        solid_time_step_size=solid_time_step_size_cls,
        time_step_size_for_acoustic_export=time_step_size_for_acoustic_export_cls,
        extrapolate_eqn_vars=extrapolate_eqn_vars_cls,
    )

