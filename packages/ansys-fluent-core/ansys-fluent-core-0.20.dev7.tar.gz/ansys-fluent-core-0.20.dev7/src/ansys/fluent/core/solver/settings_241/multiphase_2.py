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
from .outlet_number import outlet_number as outlet_number_cls
from .pressure_spec_method import pressure_spec_method as pressure_spec_method_cls
from .press_spec import press_spec as press_spec_cls
from .phase_spec import phase_spec as phase_spec_cls
from .ht_local import ht_local as ht_local_cls
from .ht_bottom import ht_bottom as ht_bottom_cls
from .den_spec import den_spec as den_spec_cls
from .granular_temperature import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration import interfacial_area_concentration as interfacial_area_concentration_cls
from .level_set_function_flux import level_set_function_flux as level_set_function_flux_cls
from .vof_spec import vof_spec as vof_spec_cls
from .volume_fraction import volume_fraction as volume_fraction_cls
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
from .wsf import wsf as wsf_cls
from .wsb import wsb as wsb_cls
from .wsn import wsn as wsn_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel', 'outlet_number', 'pressure_spec_method',
         'press_spec', 'phase_spec', 'ht_local', 'ht_bottom', 'den_spec',
         'granular_temperature', 'interfacial_area_concentration',
         'level_set_function_flux', 'vof_spec', 'volume_fraction',
         'pb_disc_bc', 'pb_disc', 'pb_qmom_bc', 'pb_qmom', 'pb_qbmm_bc',
         'pb_qbmm', 'pb_smm_bc', 'pb_smm', 'pb_dqmom_bc', 'pb_dqmom', 'wsf',
         'wsb', 'wsn']

    _child_classes = dict(
        open_channel=open_channel_cls,
        outlet_number=outlet_number_cls,
        pressure_spec_method=pressure_spec_method_cls,
        press_spec=press_spec_cls,
        phase_spec=phase_spec_cls,
        ht_local=ht_local_cls,
        ht_bottom=ht_bottom_cls,
        den_spec=den_spec_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        level_set_function_flux=level_set_function_flux_cls,
        vof_spec=vof_spec_cls,
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

