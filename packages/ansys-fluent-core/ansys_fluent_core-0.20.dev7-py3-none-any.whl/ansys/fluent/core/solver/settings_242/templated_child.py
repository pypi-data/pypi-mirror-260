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

from .name import name as name_cls
from .type_11 import type as type_cls
from .walls import walls as walls_cls
from .vector_2 import vector as vector_cls
from .center_1 import center as center_cls
from .axis_3 import axis as axis_cls
from .normalized import normalized as normalized_cls
from .fluid_zones import fluid_zones as fluid_zones_cls
from .inlets import inlets as inlets_cls
from .outlets import outlets as outlets_cls
from .fixed_value import fixed_value as fixed_value_cls
from .observable_list import observable_list as observable_list_cls
from .constant_2 import constant as constant_cls
from .combination_type import combination_type as combination_type_cls
from .entries import entries as entries_cls
from .operator import operator as operator_cls
from .observable_1 import observable as observable_cls
from .factor_1 import factor_1 as factor_1_cls
from .factor_2 import factor_2 as factor_2_cls
from .numerator import numerator as numerator_cls
from .denominator import denominator as denominator_cls
from .integral_type import integral_type as integral_type_cls
from .field_variable import field_variable as field_variable_cls
from .surfaces_11 import surfaces as surfaces_cls
from .integration_domain import integration_domain as integration_domain_cls
from .zones_7 import zones as zones_cls
from .box_bounds import box_bounds as box_bounds_cls
from .cell_register import cell_register as cell_register_cls
from .field_direction import field_direction as field_direction_cls
class templated_child(Group):
    """
    'child_object_type' of templated.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'walls', 'vector', 'center', 'axis', 'normalized',
         'fluid_zones', 'inlets', 'outlets', 'fixed_value', 'observable_list',
         'constant', 'combination_type', 'entries', 'operator', 'observable',
         'factor_1', 'factor_2', 'numerator', 'denominator', 'integral_type',
         'field_variable', 'surfaces', 'integration_domain', 'zones',
         'box_bounds', 'cell_register', 'field_direction']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        walls=walls_cls,
        vector=vector_cls,
        center=center_cls,
        axis=axis_cls,
        normalized=normalized_cls,
        fluid_zones=fluid_zones_cls,
        inlets=inlets_cls,
        outlets=outlets_cls,
        fixed_value=fixed_value_cls,
        observable_list=observable_list_cls,
        constant=constant_cls,
        combination_type=combination_type_cls,
        entries=entries_cls,
        operator=operator_cls,
        observable=observable_cls,
        factor_1=factor_1_cls,
        factor_2=factor_2_cls,
        numerator=numerator_cls,
        denominator=denominator_cls,
        integral_type=integral_type_cls,
        field_variable=field_variable_cls,
        surfaces=surfaces_cls,
        integration_domain=integration_domain_cls,
        zones=zones_cls,
        box_bounds=box_bounds_cls,
        cell_register=cell_register_cls,
        field_direction=field_direction_cls,
    )

