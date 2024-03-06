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

from .option import option as option_cls
from .cumulative_force import cumulative_force as cumulative_force_cls
from .cumulative_force_coefficient import cumulative_force_coefficient as cumulative_force_coefficient_cls
from .cumulative_moment import cumulative_moment as cumulative_moment_cls
from .cumulative_moment_coefficient import cumulative_moment_coefficient as cumulative_moment_coefficient_cls
class option(Group):
    """
    'option' child.
    """

    fluent_name = "option"

    child_names = \
        ['option', 'cumulative_force', 'cumulative_force_coefficient',
         'cumulative_moment', 'cumulative_moment_coefficient']

    _child_classes = dict(
        option=option_cls,
        cumulative_force=cumulative_force_cls,
        cumulative_force_coefficient=cumulative_force_coefficient_cls,
        cumulative_moment=cumulative_moment_cls,
        cumulative_moment_coefficient=cumulative_moment_coefficient_cls,
    )

