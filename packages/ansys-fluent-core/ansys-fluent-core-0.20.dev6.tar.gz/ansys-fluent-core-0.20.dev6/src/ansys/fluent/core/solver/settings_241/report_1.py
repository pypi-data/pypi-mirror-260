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

from .simulation_reports import simulation_reports as simulation_reports_cls
from .discrete_phase_1 import discrete_phase as discrete_phase_cls
from .fluxes import fluxes as fluxes_cls
from .flow import flow as flow_cls
from .modified_setting_options import modified_setting_options as modified_setting_options_cls
from .population_balance import population_balance as population_balance_cls
from .heat_exchanger_1 import heat_exchanger as heat_exchanger_cls
from .system import system as system_cls
from .surface_integrals import surface_integrals as surface_integrals_cls
from .volume_integrals import volume_integrals as volume_integrals_cls
from .aero_optical_distortions import aero_optical_distortions as aero_optical_distortions_cls
from .forces import forces as forces_cls
from .multiphase_summary import multiphase_summary as multiphase_summary_cls
from .particle_summary import particle_summary as particle_summary_cls
from .pathline_summary import pathline_summary as pathline_summary_cls
from .projected_surface_area import projected_surface_area as projected_surface_area_cls
from .summary_1 import summary as summary_cls
from .vbm import vbm as vbm_cls
class report(Group):
    """
    'report' child.
    """

    fluent_name = "report"

    child_names = \
        ['simulation_reports', 'discrete_phase', 'fluxes', 'flow',
         'modified_setting_options', 'population_balance', 'heat_exchanger',
         'system', 'surface_integrals', 'volume_integrals']

    command_names = \
        ['aero_optical_distortions', 'forces', 'multiphase_summary',
         'particle_summary', 'pathline_summary', 'projected_surface_area',
         'summary', 'vbm']

    _child_classes = dict(
        simulation_reports=simulation_reports_cls,
        discrete_phase=discrete_phase_cls,
        fluxes=fluxes_cls,
        flow=flow_cls,
        modified_setting_options=modified_setting_options_cls,
        population_balance=population_balance_cls,
        heat_exchanger=heat_exchanger_cls,
        system=system_cls,
        surface_integrals=surface_integrals_cls,
        volume_integrals=volume_integrals_cls,
        aero_optical_distortions=aero_optical_distortions_cls,
        forces=forces_cls,
        multiphase_summary=multiphase_summary_cls,
        particle_summary=particle_summary_cls,
        pathline_summary=pathline_summary_cls,
        projected_surface_area=projected_surface_area_cls,
        summary=summary_cls,
        vbm=vbm_cls,
    )

