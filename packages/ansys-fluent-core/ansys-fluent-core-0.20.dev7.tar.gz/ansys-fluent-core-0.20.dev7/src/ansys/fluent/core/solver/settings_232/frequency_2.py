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

from .option_14 import option as option_cls
from .iterations_1 import iterations as iterations_cls
from .time_steps import time_steps as time_steps_cls
class frequency(Group):
    """
    Define the frequency at which cells in the register are marked for poor mesh numerics treatment.
    """

    fluent_name = "frequency"

    child_names = \
        ['option', 'iterations', 'time_steps']

    _child_classes = dict(
        option=option_cls,
        iterations=iterations_cls,
        time_steps=time_steps_cls,
    )

