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

from .lookup_table import lookup_table as lookup_table_cls
from .composition_type import composition_type as composition_type_cls
from .species_fractions import species_fractions as species_fractions_cls
from .pressure_points import pressure_points as pressure_points_cls
from .pressure_minimum import pressure_minimum as pressure_minimum_cls
from .pressure_maximum import pressure_maximum as pressure_maximum_cls
from .temperature_points import temperature_points as temperature_points_cls
from .temperature_minimum import temperature_minimum as temperature_minimum_cls
from .temperature_maximum import temperature_maximum as temperature_maximum_cls
class real_gas_nist_mixture(Group):
    """
    'real_gas_nist_mixture' child.
    """

    fluent_name = "real-gas-nist-mixture"

    child_names = \
        ['lookup_table', 'composition_type', 'species_fractions',
         'pressure_points', 'pressure_minimum', 'pressure_maximum',
         'temperature_points', 'temperature_minimum', 'temperature_maximum']

    _child_classes = dict(
        lookup_table=lookup_table_cls,
        composition_type=composition_type_cls,
        species_fractions=species_fractions_cls,
        pressure_points=pressure_points_cls,
        pressure_minimum=pressure_minimum_cls,
        pressure_maximum=pressure_maximum_cls,
        temperature_points=temperature_points_cls,
        temperature_minimum=temperature_minimum_cls,
        temperature_maximum=temperature_maximum_cls,
    )

