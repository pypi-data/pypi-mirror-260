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

from .load_balancing import load_balancing as load_balancing_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls
class dpm_load_balancing(Group):
    """
    Enable automatic load balancing for DPM.
    """

    fluent_name = "dpm-load-balancing"

    child_names = \
        ['load_balancing', 'threshold', 'interval']

    _child_classes = dict(
        load_balancing=load_balancing_cls,
        threshold=threshold_cls,
        interval=interval_cls,
    )

