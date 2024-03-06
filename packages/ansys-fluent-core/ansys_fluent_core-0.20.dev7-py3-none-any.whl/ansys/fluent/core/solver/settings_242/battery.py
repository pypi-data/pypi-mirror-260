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

from .enabled_13 import enabled as enabled_cls
from .solution_method_1 import solution_method as solution_method_cls
from .echem_model import echem_model as echem_model_cls
from .zone_assignment_1 import zone_assignment as zone_assignment_cls
from .ntgk_model_settings import ntgk_model_settings as ntgk_model_settings_cls
from .ecm_model_settings import ecm_model_settings as ecm_model_settings_cls
from .p2d_model_settings import p2d_model_settings as p2d_model_settings_cls
from .customized_echem_model_settings import customized_echem_model_settings as customized_echem_model_settings_cls
from .cht_model_settings import cht_model_settings as cht_model_settings_cls
from .fmu_model_settings import fmu_model_settings as fmu_model_settings_cls
from .eload_condition import eload_condition as eload_condition_cls
from .solution_option import solution_option as solution_option_cls
from .advanced_models import advanced_models as advanced_models_cls
from .tool_kits import tool_kits as tool_kits_cls
class battery(Group):
    """
    Battery model settings.
    """

    fluent_name = "battery"

    child_names = \
        ['enabled', 'solution_method', 'echem_model', 'zone_assignment',
         'ntgk_model_settings', 'ecm_model_settings', 'p2d_model_settings',
         'customized_echem_model_settings', 'cht_model_settings',
         'fmu_model_settings', 'eload_condition', 'solution_option',
         'advanced_models', 'tool_kits']

    _child_classes = dict(
        enabled=enabled_cls,
        solution_method=solution_method_cls,
        echem_model=echem_model_cls,
        zone_assignment=zone_assignment_cls,
        ntgk_model_settings=ntgk_model_settings_cls,
        ecm_model_settings=ecm_model_settings_cls,
        p2d_model_settings=p2d_model_settings_cls,
        customized_echem_model_settings=customized_echem_model_settings_cls,
        cht_model_settings=cht_model_settings_cls,
        fmu_model_settings=fmu_model_settings_cls,
        eload_condition=eload_condition_cls,
        solution_option=solution_option_cls,
        advanced_models=advanced_models_cls,
        tool_kits=tool_kits_cls,
    )

