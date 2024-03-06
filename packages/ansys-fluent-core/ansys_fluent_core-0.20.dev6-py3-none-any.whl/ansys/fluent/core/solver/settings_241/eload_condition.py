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

from .eload_type import eload_type as eload_type_cls
from .crate_value import crate_value as crate_value_cls
from .current_value import current_value as current_value_cls
from .voltage_value import voltage_value as voltage_value_cls
from .power_value import power_value as power_value_cls
from .external_resistance import external_resistance as external_resistance_cls
from .profile_type import profile_type as profile_type_cls
from .profile_file import profile_file as profile_file_cls
from .udf_profile_name import udf_profile_name as udf_profile_name_cls
class eload_condition(Group):
    """
    'eload_condition' child.
    """

    fluent_name = "eload-condition"

    child_names = \
        ['eload_type', 'crate_value', 'current_value', 'voltage_value',
         'power_value', 'external_resistance', 'profile_type', 'profile_file',
         'udf_profile_name']

    _child_classes = dict(
        eload_type=eload_type_cls,
        crate_value=crate_value_cls,
        current_value=current_value_cls,
        voltage_value=voltage_value_cls,
        power_value=power_value_cls,
        external_resistance=external_resistance_cls,
        profile_type=profile_type_cls,
        profile_file=profile_file_cls,
        udf_profile_name=udf_profile_name_cls,
    )

