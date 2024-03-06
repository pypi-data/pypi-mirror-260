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

from .material_1 import material as material_cls
from .participates_in_radiation import participates_in_radiation as participates_in_radiation_cls
class general(Group):
    """
    Set settings of selected variable.
    """

    fluent_name = "general"

    child_names = \
        ['material', 'participates_in_radiation']

    _child_classes = dict(
        material=material_cls,
        participates_in_radiation=participates_in_radiation_cls,
    )

