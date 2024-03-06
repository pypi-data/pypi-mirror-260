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

from .thermal_effects_1 import thermal_effects as thermal_effects_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['thermal_effects']

    _child_classes = dict(
        thermal_effects=thermal_effects_cls,
    )

