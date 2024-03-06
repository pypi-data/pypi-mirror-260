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

from .thermal_expansion_0 import thermal_expansion_0 as thermal_expansion_0_cls
from .thermal_expansion_1 import thermal_expansion_1 as thermal_expansion_1_cls
from .thermal_expansion_2 import thermal_expansion_2 as thermal_expansion_2_cls
class orthotropic_structure_te(Group):
    """
    'orthotropic_structure_te' child.
    """

    fluent_name = "orthotropic-structure-te"

    child_names = \
        ['thermal_expansion_0', 'thermal_expansion_1', 'thermal_expansion_2']

    _child_classes = dict(
        thermal_expansion_0=thermal_expansion_0_cls,
        thermal_expansion_1=thermal_expansion_1_cls,
        thermal_expansion_2=thermal_expansion_2_cls,
    )

