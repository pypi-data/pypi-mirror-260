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
from .update_sources_every_flow_iteration import update_sources_every_flow_iteration as update_sources_every_flow_iteration_cls
from .iteration_interval import iteration_interval as iteration_interval_cls
class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['option', 'update_sources_every_flow_iteration',
         'iteration_interval']

    _child_classes = dict(
        option=option_cls,
        update_sources_every_flow_iteration=update_sources_every_flow_iteration_cls,
        iteration_interval=iteration_interval_cls,
    )

