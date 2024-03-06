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

from .convective_heat_transfer import convective_heat_transfer as convective_heat_transfer_cls
from .include_convective_heat_transfer import include_convective_heat_transfer as include_convective_heat_transfer_cls
from .film_movement import film_movement as film_movement_cls
from .film_adds_to_dpm_concentration import film_adds_to_dpm_concentration as film_adds_to_dpm_concentration_cls
from .temperature_limiter import temperature_limiter as temperature_limiter_cls
class wall_film(Group):
    """
    'wall_film' child.
    """

    fluent_name = "wall-film"

    child_names = \
        ['convective_heat_transfer', 'include_convective_heat_transfer',
         'film_movement', 'film_adds_to_dpm_concentration',
         'temperature_limiter']

    _child_classes = dict(
        convective_heat_transfer=convective_heat_transfer_cls,
        include_convective_heat_transfer=include_convective_heat_transfer_cls,
        film_movement=film_movement_cls,
        film_adds_to_dpm_concentration=film_adds_to_dpm_concentration_cls,
        temperature_limiter=temperature_limiter_cls,
    )

