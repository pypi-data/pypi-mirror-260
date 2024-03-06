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

from .option_10 import option as option_cls
from .value import value as value_cls
from .single_rate import single_rate as single_rate_cls
from .two_competing_rates import two_competing_rates as two_competing_rates_cls
from .cpd_model import cpd_model as cpd_model_cls
class devolatilization_model(Group):
    """
    'devolatilization_model' child.
    """

    fluent_name = "devolatilization-model"

    child_names = \
        ['option', 'value', 'single_rate', 'two_competing_rates', 'cpd_model']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        single_rate=single_rate_cls,
        two_competing_rates=two_competing_rates_cls,
        cpd_model=cpd_model_cls,
    )

