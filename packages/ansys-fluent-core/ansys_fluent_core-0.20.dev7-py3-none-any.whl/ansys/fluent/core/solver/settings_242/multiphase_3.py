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

from .open_channel import open_channel as open_channel_cls
from .inlet_number import inlet_number as inlet_number_cls
from .phase_spec_1 import phase_spec as phase_spec_cls
from .flow_spec import flow_spec as flow_spec_cls
from .free_surface_level import free_surface_level as free_surface_level_cls
from .ht_bottom import ht_bottom as ht_bottom_cls
from .ht_total import ht_total as ht_total_cls
from .vmag import vmag as vmag_cls
from .den_spec import den_spec as den_spec_cls
from .granular_temperature_1 import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration_1 import interfacial_area_concentration as interfacial_area_concentration_cls
from .level_set_function_flux_1 import level_set_function_flux as level_set_function_flux_cls
from .volume_fraction_1 import volume_fraction as volume_fraction_cls
from .pb_disc_bc import pb_disc_bc as pb_disc_bc_cls
from .pb_disc import pb_disc as pb_disc_cls
from .pb_qmom_bc import pb_qmom_bc as pb_qmom_bc_cls
from .pb_qmom import pb_qmom as pb_qmom_cls
from .pb_qbmm_bc import pb_qbmm_bc as pb_qbmm_bc_cls
from .pb_qbmm import pb_qbmm as pb_qbmm_cls
from .pb_smm_bc import pb_smm_bc as pb_smm_bc_cls
from .pb_smm import pb_smm as pb_smm_cls
from .pb_dqmom_bc import pb_dqmom_bc as pb_dqmom_bc_cls
from .pb_dqmom import pb_dqmom as pb_dqmom_cls
from .wsf_1 import wsf as wsf_cls
from .wsb_1 import wsb as wsb_cls
from .wsn_1 import wsn as wsn_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel', 'inlet_number', 'phase_spec', 'flow_spec',
         'free_surface_level', 'ht_bottom', 'ht_total', 'vmag', 'den_spec',
         'granular_temperature', 'interfacial_area_concentration',
         'level_set_function_flux', 'volume_fraction', 'pb_disc_bc',
         'pb_disc', 'pb_qmom_bc', 'pb_qmom', 'pb_qbmm_bc', 'pb_qbmm',
         'pb_smm_bc', 'pb_smm', 'pb_dqmom_bc', 'pb_dqmom', 'wsf', 'wsb',
         'wsn']

    _child_classes = dict(
        open_channel=open_channel_cls,
        inlet_number=inlet_number_cls,
        phase_spec=phase_spec_cls,
        flow_spec=flow_spec_cls,
        free_surface_level=free_surface_level_cls,
        ht_bottom=ht_bottom_cls,
        ht_total=ht_total_cls,
        vmag=vmag_cls,
        den_spec=den_spec_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        level_set_function_flux=level_set_function_flux_cls,
        volume_fraction=volume_fraction_cls,
        pb_disc_bc=pb_disc_bc_cls,
        pb_disc=pb_disc_cls,
        pb_qmom_bc=pb_qmom_bc_cls,
        pb_qmom=pb_qmom_cls,
        pb_qbmm_bc=pb_qbmm_bc_cls,
        pb_qbmm=pb_qbmm_cls,
        pb_smm_bc=pb_smm_bc_cls,
        pb_smm=pb_smm_cls,
        pb_dqmom_bc=pb_dqmom_bc_cls,
        pb_dqmom=pb_dqmom_cls,
        wsf=wsf_cls,
        wsb=wsb_cls,
        wsn=wsn_cls,
    )

