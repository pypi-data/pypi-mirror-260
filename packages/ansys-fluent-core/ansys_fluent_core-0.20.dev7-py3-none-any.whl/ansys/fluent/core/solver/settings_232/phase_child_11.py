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

from .name_2 import name as name_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature_1 import temperature as temperature_cls
from .q import q as q_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'thermal_bc', 'temperature', 'q']

    _child_classes = dict(
        name=name_cls,
        thermal_bc=thermal_bc_cls,
        temperature=temperature_cls,
        q=q_cls,
    )

