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

from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature_1 import temperature as temperature_cls
from .q import q as q_cls
class network_end(Group):
    """
    Help not available.
    """

    fluent_name = "network-end"

    child_names = \
        ['thermal_bc', 'temperature', 'q']

    _child_classes = dict(
        thermal_bc=thermal_bc_cls,
        temperature=temperature_cls,
        q=q_cls,
    )

