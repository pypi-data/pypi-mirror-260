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

from .delay_model_change_update import delay_model_change_update as delay_model_change_update_cls
from .batch_thread_update import batch_thread_update as batch_thread_update_cls
class advanced(Group):
    """
    Control settings while doing BC setup.
    """

    fluent_name = "advanced"

    child_names = \
        ['delay_model_change_update', 'batch_thread_update']

    _child_classes = dict(
        delay_model_change_update=delay_model_change_update_cls,
        batch_thread_update=batch_thread_update_cls,
    )

