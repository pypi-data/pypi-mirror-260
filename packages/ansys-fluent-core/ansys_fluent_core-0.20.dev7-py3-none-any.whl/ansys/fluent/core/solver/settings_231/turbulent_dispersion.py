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

from .option_3 import option as option_cls
from .random_eddy_lifetime import random_eddy_lifetime as random_eddy_lifetime_cls
from .number_of_tries import number_of_tries as number_of_tries_cls
from .time_scale_constant import time_scale_constant as time_scale_constant_cls
class turbulent_dispersion(Group):
    """
    'turbulent_dispersion' child.
    """

    fluent_name = "turbulent-dispersion"

    child_names = \
        ['option', 'random_eddy_lifetime', 'number_of_tries',
         'time_scale_constant']

    _child_classes = dict(
        option=option_cls,
        random_eddy_lifetime=random_eddy_lifetime_cls,
        number_of_tries=number_of_tries_cls,
        time_scale_constant=time_scale_constant_cls,
    )

