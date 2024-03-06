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

from .htc import htc as htc_cls
from .unsteady_statistics import unsteady_statistics as unsteady_statistics_cls
from .user_defined_coupling_variables_via_udm import user_defined_coupling_variables_via_udm as user_defined_coupling_variables_via_udm_cls
from .use_face_or_element_based_data_transfer import use_face_or_element_based_data_transfer as use_face_or_element_based_data_transfer_cls
from .activate_flow_boundary_coupling_model import activate_flow_boundary_coupling_model as activate_flow_boundary_coupling_model_cls
from .write_scp_file import write_scp_file as write_scp_file_cls
from .connect_parallel import connect_parallel as connect_parallel_cls
from .init_and_solve import init_and_solve as init_and_solve_cls
from .solve import solve as solve_cls
class system_coupling(Group):
    """
    Enter the system coupling model menu.
    """

    fluent_name = "system-coupling"

    child_names = \
        ['htc', 'unsteady_statistics',
         'user_defined_coupling_variables_via_udm',
         'use_face_or_element_based_data_transfer',
         'activate_flow_boundary_coupling_model']

    command_names = \
        ['write_scp_file', 'connect_parallel', 'init_and_solve', 'solve']

    _child_classes = dict(
        htc=htc_cls,
        unsteady_statistics=unsteady_statistics_cls,
        user_defined_coupling_variables_via_udm=user_defined_coupling_variables_via_udm_cls,
        use_face_or_element_based_data_transfer=use_face_or_element_based_data_transfer_cls,
        activate_flow_boundary_coupling_model=activate_flow_boundary_coupling_model_cls,
        write_scp_file=write_scp_file_cls,
        connect_parallel=connect_parallel_cls,
        init_and_solve=init_and_solve_cls,
        solve=solve_cls,
    )

