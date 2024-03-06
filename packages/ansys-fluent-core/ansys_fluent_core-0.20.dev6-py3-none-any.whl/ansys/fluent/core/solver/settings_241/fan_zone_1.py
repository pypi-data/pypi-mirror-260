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

from .fan_zone import fan_zone as fan_zone_cls
from .inlet_fan_zone import inlet_fan_zone as inlet_fan_zone_cls
from .fan_thickness import fan_thickness as fan_thickness_cls
from .fan_hub_rad import fan_hub_rad as fan_hub_rad_cls
from .fan_tip_rad import fan_tip_rad as fan_tip_rad_cls
from .fan_origin import fan_origin as fan_origin_cls
from .fan_rot_dir import fan_rot_dir as fan_rot_dir_cls
from .fan_opert_angvel import fan_opert_angvel as fan_opert_angvel_cls
from .fan_inflection_point import fan_inflection_point as fan_inflection_point_cls
from .limit_flow_fan import limit_flow_fan as limit_flow_fan_cls
from .max_flow_rate import max_flow_rate as max_flow_rate_cls
from .min_flow_rate import min_flow_rate as min_flow_rate_cls
from .tan_source_term import tan_source_term as tan_source_term_cls
from .rad_source_term import rad_source_term as rad_source_term_cls
from .axial_source_term import axial_source_term as axial_source_term_cls
from .fan_axial_source_method import fan_axial_source_method as fan_axial_source_method_cls
from .fan_pre_jump import fan_pre_jump as fan_pre_jump_cls
from .fan_curve_fit import fan_curve_fit as fan_curve_fit_cls
from .fan_poly_order import fan_poly_order as fan_poly_order_cls
from .fan_ini_flow import fan_ini_flow as fan_ini_flow_cls
from .fan_test_angvel import fan_test_angvel as fan_test_angvel_cls
from .fan_test_temp import fan_test_temp as fan_test_temp_cls
from .fan_curve_filename import fan_curve_filename as fan_curve_filename_cls
from .read_fan_curve import read_fan_curve as read_fan_curve_cls
class fan_zone(Group):
    """
    Help not available.
    """

    fluent_name = "fan-zone"

    child_names = \
        ['fan_zone', 'inlet_fan_zone', 'fan_thickness', 'fan_hub_rad',
         'fan_tip_rad', 'fan_origin', 'fan_rot_dir', 'fan_opert_angvel',
         'fan_inflection_point', 'limit_flow_fan', 'max_flow_rate',
         'min_flow_rate', 'tan_source_term', 'rad_source_term',
         'axial_source_term', 'fan_axial_source_method', 'fan_pre_jump',
         'fan_curve_fit', 'fan_poly_order', 'fan_ini_flow', 'fan_test_angvel',
         'fan_test_temp', 'fan_curve_filename', 'read_fan_curve']

    _child_classes = dict(
        fan_zone=fan_zone_cls,
        inlet_fan_zone=inlet_fan_zone_cls,
        fan_thickness=fan_thickness_cls,
        fan_hub_rad=fan_hub_rad_cls,
        fan_tip_rad=fan_tip_rad_cls,
        fan_origin=fan_origin_cls,
        fan_rot_dir=fan_rot_dir_cls,
        fan_opert_angvel=fan_opert_angvel_cls,
        fan_inflection_point=fan_inflection_point_cls,
        limit_flow_fan=limit_flow_fan_cls,
        max_flow_rate=max_flow_rate_cls,
        min_flow_rate=min_flow_rate_cls,
        tan_source_term=tan_source_term_cls,
        rad_source_term=rad_source_term_cls,
        axial_source_term=axial_source_term_cls,
        fan_axial_source_method=fan_axial_source_method_cls,
        fan_pre_jump=fan_pre_jump_cls,
        fan_curve_fit=fan_curve_fit_cls,
        fan_poly_order=fan_poly_order_cls,
        fan_ini_flow=fan_ini_flow_cls,
        fan_test_angvel=fan_test_angvel_cls,
        fan_test_temp=fan_test_temp_cls,
        fan_curve_filename=fan_curve_filename_cls,
        read_fan_curve=read_fan_curve_cls,
    )

