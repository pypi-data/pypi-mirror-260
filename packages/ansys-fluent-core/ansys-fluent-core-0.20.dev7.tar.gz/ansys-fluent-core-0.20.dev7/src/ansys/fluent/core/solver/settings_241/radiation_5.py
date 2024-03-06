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

from .band_in_emiss import band_in_emiss as band_in_emiss_cls
from .radiation_bc import radiation_bc as radiation_bc_cls
from .mc_bsource_p import mc_bsource_p as mc_bsource_p_cls
from .mc_poldfun_p import mc_poldfun_p as mc_poldfun_p_cls
from .polar_func_type import polar_func_type as polar_func_type_cls
from .mc_polar_expr import mc_polar_expr as mc_polar_expr_cls
from .polar_pair_list import polar_pair_list as polar_pair_list_cls
from .pold_pair_list_rad import pold_pair_list_rad as pold_pair_list_rad_cls
from .radiation_direction import radiation_direction as radiation_direction_cls
from .coll_dtheta import coll_dtheta as coll_dtheta_cls
from .coll_dphi import coll_dphi as coll_dphi_cls
from .band_q_irrad import band_q_irrad as band_q_irrad_cls
from .band_q_irrad_diffuse import band_q_irrad_diffuse as band_q_irrad_diffuse_cls
from .band_diffuse_frac import band_diffuse_frac as band_diffuse_frac_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
from .critical_zone import critical_zone as critical_zone_cls
from .fpsc import fpsc as fpsc_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_direction import solar_direction as solar_direction_cls
from .solar_irradiation import solar_irradiation as solar_irradiation_cls
from .v_transmissivity import v_transmissivity as v_transmissivity_cls
from .ir_transmissivity import ir_transmissivity as ir_transmissivity_cls
from .v_opq_absorbtivity import v_opq_absorbtivity as v_opq_absorbtivity_cls
from .ir_opq_absorbtivity import ir_opq_absorbtivity as ir_opq_absorbtivity_cls
from .v_st_absorbtivity import v_st_absorbtivity as v_st_absorbtivity_cls
from .ir_st_absorbtivity import ir_st_absorbtivity as ir_st_absorbtivity_cls
from .d_st_absorbtivity import d_st_absorbtivity as d_st_absorbtivity_cls
from .d_transmissivity import d_transmissivity as d_transmissivity_cls
class radiation(Group):
    """
    Help not available.
    """

    fluent_name = "radiation"

    child_names = \
        ['band_in_emiss', 'radiation_bc', 'mc_bsource_p', 'mc_poldfun_p',
         'polar_func_type', 'mc_polar_expr', 'polar_pair_list',
         'pold_pair_list_rad', 'radiation_direction', 'coll_dtheta',
         'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'band_diffuse_frac', 'radiating_s2s_surface', 'critical_zone',
         'fpsc', 'parallel_collimated_beam', 'solar_fluxes',
         'solar_direction', 'solar_irradiation', 'v_transmissivity',
         'ir_transmissivity', 'v_opq_absorbtivity', 'ir_opq_absorbtivity',
         'v_st_absorbtivity', 'ir_st_absorbtivity', 'd_st_absorbtivity',
         'd_transmissivity']

    _child_classes = dict(
        band_in_emiss=band_in_emiss_cls,
        radiation_bc=radiation_bc_cls,
        mc_bsource_p=mc_bsource_p_cls,
        mc_poldfun_p=mc_poldfun_p_cls,
        polar_func_type=polar_func_type_cls,
        mc_polar_expr=mc_polar_expr_cls,
        polar_pair_list=polar_pair_list_cls,
        pold_pair_list_rad=pold_pair_list_rad_cls,
        radiation_direction=radiation_direction_cls,
        coll_dtheta=coll_dtheta_cls,
        coll_dphi=coll_dphi_cls,
        band_q_irrad=band_q_irrad_cls,
        band_q_irrad_diffuse=band_q_irrad_diffuse_cls,
        band_diffuse_frac=band_diffuse_frac_cls,
        radiating_s2s_surface=radiating_s2s_surface_cls,
        critical_zone=critical_zone_cls,
        fpsc=fpsc_cls,
        parallel_collimated_beam=parallel_collimated_beam_cls,
        solar_fluxes=solar_fluxes_cls,
        solar_direction=solar_direction_cls,
        solar_irradiation=solar_irradiation_cls,
        v_transmissivity=v_transmissivity_cls,
        ir_transmissivity=ir_transmissivity_cls,
        v_opq_absorbtivity=v_opq_absorbtivity_cls,
        ir_opq_absorbtivity=ir_opq_absorbtivity_cls,
        v_st_absorbtivity=v_st_absorbtivity_cls,
        ir_st_absorbtivity=ir_st_absorbtivity_cls,
        d_st_absorbtivity=d_st_absorbtivity_cls,
        d_transmissivity=d_transmissivity_cls,
    )

