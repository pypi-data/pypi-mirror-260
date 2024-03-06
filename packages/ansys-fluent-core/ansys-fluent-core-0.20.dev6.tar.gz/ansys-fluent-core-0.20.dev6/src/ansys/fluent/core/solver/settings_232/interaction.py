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

from .option_2 import option as option_cls
from .source_update_every_iteration_enabled import source_update_every_iteration_enabled as source_update_every_iteration_enabled_cls
from .iteration_interval import iteration_interval as iteration_interval_cls
class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['option', 'source_update_every_iteration_enabled',
         'iteration_interval']

    _child_classes = dict(
        option=option_cls,
        source_update_every_iteration_enabled=source_update_every_iteration_enabled_cls,
        iteration_interval=iteration_interval_cls,
    )

