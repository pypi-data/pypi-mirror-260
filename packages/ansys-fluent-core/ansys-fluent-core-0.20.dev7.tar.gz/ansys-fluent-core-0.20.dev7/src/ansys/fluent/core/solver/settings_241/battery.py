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

from .enabled_12 import enabled as enabled_cls
from .solution_method_1 import solution_method as solution_method_cls
from .echem_model import echem_model as echem_model_cls
from .zone_assignment_1 import zone_assignment as zone_assignment_cls
from .contact_resistance import contact_resistance as contact_resistance_cls
from .ntgk_model_settings import ntgk_model_settings as ntgk_model_settings_cls
from .ecm_model_settings import ecm_model_settings as ecm_model_settings_cls
from .p2d_model_settings import p2d_model_settings as p2d_model_settings_cls
from .eload_condition import eload_condition as eload_condition_cls
from .echem_stop_criterion import echem_stop_criterion as echem_stop_criterion_cls
from .cell_clustering import cell_clustering as cell_clustering_cls
from .solution_option import solution_option as solution_option_cls
from .life_model import life_model as life_model_cls
from .swelling_model import swelling_model as swelling_model_cls
from .thermal_abuse_model import thermal_abuse_model as thermal_abuse_model_cls
from .pack_builder import pack_builder as pack_builder_cls
from .rom_tool_kit import rom_tool_kit as rom_tool_kit_cls
from .orthotropic_k import orthotropic_k as orthotropic_k_cls
from .udf_hooks import udf_hooks as udf_hooks_cls
from .parameter_estimation_tool import parameter_estimation_tool as parameter_estimation_tool_cls
from .standalone_echem_model import standalone_echem_model as standalone_echem_model_cls
class battery(Group):
    """
    'battery' child.
    """

    fluent_name = "battery"

    child_names = \
        ['enabled', 'solution_method', 'echem_model', 'zone_assignment',
         'contact_resistance', 'ntgk_model_settings', 'ecm_model_settings',
         'p2d_model_settings', 'eload_condition', 'echem_stop_criterion',
         'cell_clustering', 'solution_option', 'life_model', 'swelling_model',
         'thermal_abuse_model', 'pack_builder', 'rom_tool_kit',
         'orthotropic_k', 'udf_hooks']

    command_names = \
        ['parameter_estimation_tool', 'standalone_echem_model']

    _child_classes = dict(
        enabled=enabled_cls,
        solution_method=solution_method_cls,
        echem_model=echem_model_cls,
        zone_assignment=zone_assignment_cls,
        contact_resistance=contact_resistance_cls,
        ntgk_model_settings=ntgk_model_settings_cls,
        ecm_model_settings=ecm_model_settings_cls,
        p2d_model_settings=p2d_model_settings_cls,
        eload_condition=eload_condition_cls,
        echem_stop_criterion=echem_stop_criterion_cls,
        cell_clustering=cell_clustering_cls,
        solution_option=solution_option_cls,
        life_model=life_model_cls,
        swelling_model=swelling_model_cls,
        thermal_abuse_model=thermal_abuse_model_cls,
        pack_builder=pack_builder_cls,
        rom_tool_kit=rom_tool_kit_cls,
        orthotropic_k=orthotropic_k_cls,
        udf_hooks=udf_hooks_cls,
        parameter_estimation_tool=parameter_estimation_tool_cls,
        standalone_echem_model=standalone_echem_model_cls,
    )

