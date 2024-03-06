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

from .enabled_20 import enabled as enabled_cls
from .capacity_fade_table import capacity_fade_table as capacity_fade_table_cls
class capacity_fade_model(Group):
    """
    Set capacity fade model.
    """

    fluent_name = "capacity-fade-model"

    child_names = \
        ['enabled', 'capacity_fade_table']

    _child_classes = dict(
        enabled=enabled_cls,
        capacity_fade_table=capacity_fade_table_cls,
    )

