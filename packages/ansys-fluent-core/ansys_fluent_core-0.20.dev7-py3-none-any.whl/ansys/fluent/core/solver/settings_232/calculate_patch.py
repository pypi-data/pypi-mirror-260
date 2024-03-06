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

from .domain import domain as domain_cls
from .cell_zones import cell_zones as cell_zones_cls
from .register_id import register_id as register_id_cls
from .variable import variable as variable_cls
from .patch_velocity import patch_velocity as patch_velocity_cls
from .use_custom_field_function import use_custom_field_function as use_custom_field_function_cls
from .custom_field_function_name import custom_field_function_name as custom_field_function_name_cls
from .value_1 import value as value_cls
class calculate_patch(Command):
    """
    Patch a value for a flow variable in the domain.
    
    Parameters
    ----------
        domain : str
            'domain' child.
        cell_zones : typing.List[str]
            'cell_zones' child.
        register_id : typing.List[str]
            'register_id' child.
        variable : str
            'variable' child.
        patch_velocity : bool
            'patch_velocity' child.
        use_custom_field_function : bool
            'use_custom_field_function' child.
        custom_field_function_name : str
            'custom_field_function_name' child.
        value : real
            'value' child.
    
    """

    fluent_name = "calculate-patch"

    argument_names = \
        ['domain', 'cell_zones', 'register_id', 'variable', 'patch_velocity',
         'use_custom_field_function', 'custom_field_function_name', 'value']

    _child_classes = dict(
        domain=domain_cls,
        cell_zones=cell_zones_cls,
        register_id=register_id_cls,
        variable=variable_cls,
        patch_velocity=patch_velocity_cls,
        use_custom_field_function=use_custom_field_function_cls,
        custom_field_function_name=custom_field_function_name_cls,
        value=value_cls,
    )

