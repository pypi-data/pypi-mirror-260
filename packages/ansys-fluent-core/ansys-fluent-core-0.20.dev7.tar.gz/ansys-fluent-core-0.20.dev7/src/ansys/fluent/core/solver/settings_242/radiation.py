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

from .model_2 import model as model_cls
from .discrete_ordinates import discrete_ordinates as discrete_ordinates_cls
from .monte_carlo import monte_carlo as monte_carlo_cls
from .s2s import s2s as s2s_cls
from .multiband import multiband as multiband_cls
from .solve_frequency import solve_frequency as solve_frequency_cls
from .solar_load import solar_load as solar_load_cls
class radiation(Group):
    """
    Model for radiative heat-transfer.
    """

    fluent_name = "radiation"

    child_names = \
        ['model', 'discrete_ordinates', 'monte_carlo', 's2s', 'multiband',
         'solve_frequency', 'solar_load']

    _child_classes = dict(
        model=model_cls,
        discrete_ordinates=discrete_ordinates_cls,
        monte_carlo=monte_carlo_cls,
        s2s=s2s_cls,
        multiband=multiband_cls,
        solve_frequency=solve_frequency_cls,
        solar_load=solar_load_cls,
    )

