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

from .enabled_26 import enabled as enabled_cls
from .model_parameters import model_parameters as model_parameters_cls
from .electrochemistry import electrochemistry as electrochemistry_cls
from .electrolyte_porous import electrolyte_porous as electrolyte_porous_cls
from .electric_field import electric_field as electric_field_cls
from .customized_udf import customized_udf as customized_udf_cls
class sofc(Group):
    """
    Enter SOFC model settings.
    """

    fluent_name = "sofc"

    child_names = \
        ['enabled', 'model_parameters', 'electrochemistry',
         'electrolyte_porous', 'electric_field', 'customized_udf']

    _child_classes = dict(
        enabled=enabled_cls,
        model_parameters=model_parameters_cls,
        electrochemistry=electrochemistry_cls,
        electrolyte_porous=electrolyte_porous_cls,
        electric_field=electric_field_cls,
        customized_udf=customized_udf_cls,
    )

