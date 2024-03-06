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

from .solar_model import solar_model as solar_model_cls
from .sun_direction_vector import sun_direction_vector as sun_direction_vector_cls
from .illumination_parameters import illumination_parameters as illumination_parameters_cls
from .quad_tree_parameters import quad_tree_parameters as quad_tree_parameters_cls
from .ground_reflectivity import ground_reflectivity as ground_reflectivity_cls
from .scattering_fraction import scattering_fraction as scattering_fraction_cls
from .solar_on_adjacent_fluid import solar_on_adjacent_fluid as solar_on_adjacent_fluid_cls
from .direction_from_solar_calculator import direction_from_solar_calculator as direction_from_solar_calculator_cls
from .solar_load_frequency import solar_load_frequency as solar_load_frequency_cls
from .solar_calculator import solar_calculator as solar_calculator_cls
from .apply_full_solar_irradiation import apply_full_solar_irradiation as apply_full_solar_irradiation_cls
from .autoread_solar_data import autoread_solar_data as autoread_solar_data_cls
from .autosave_solar_data import autosave_solar_data as autosave_solar_data_cls
from .solar_on_demand import solar_on_demand as solar_on_demand_cls
class solar_load(Group):
    """
    'solar_load' child.
    """

    fluent_name = "solar-load"

    child_names = \
        ['solar_model', 'sun_direction_vector', 'illumination_parameters',
         'quad_tree_parameters', 'ground_reflectivity', 'scattering_fraction',
         'solar_on_adjacent_fluid', 'direction_from_solar_calculator',
         'solar_load_frequency', 'solar_calculator',
         'apply_full_solar_irradiation', 'autoread_solar_data',
         'autosave_solar_data']

    command_names = \
        ['solar_on_demand']

    _child_classes = dict(
        solar_model=solar_model_cls,
        sun_direction_vector=sun_direction_vector_cls,
        illumination_parameters=illumination_parameters_cls,
        quad_tree_parameters=quad_tree_parameters_cls,
        ground_reflectivity=ground_reflectivity_cls,
        scattering_fraction=scattering_fraction_cls,
        solar_on_adjacent_fluid=solar_on_adjacent_fluid_cls,
        direction_from_solar_calculator=direction_from_solar_calculator_cls,
        solar_load_frequency=solar_load_frequency_cls,
        solar_calculator=solar_calculator_cls,
        apply_full_solar_irradiation=apply_full_solar_irradiation_cls,
        autoread_solar_data=autoread_solar_data_cls,
        autosave_solar_data=autosave_solar_data_cls,
        solar_on_demand=solar_on_demand_cls,
    )

