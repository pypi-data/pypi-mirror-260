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

from .phase_11 import phase as phase_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature import temperature as temperature_cls
from .q import q as q_cls
class network_end_child(Group):
    """
    'child_object_type' of network_end.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'thermal_bc', 'temperature', 'q']

    _child_classes = dict(
        phase=phase_cls,
        thermal_bc=thermal_bc_cls,
        temperature=temperature_cls,
        q=q_cls,
    )

