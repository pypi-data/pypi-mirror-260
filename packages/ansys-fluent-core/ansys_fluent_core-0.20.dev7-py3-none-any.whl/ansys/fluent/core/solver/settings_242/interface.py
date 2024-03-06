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

from .non_overlap_zone_name import non_overlap_zone_name as non_overlap_zone_name_cls
class interface(Group):
    """
    Help not available.
    """

    fluent_name = "interface"

    child_names = \
        ['non_overlap_zone_name']

    _child_classes = dict(
        non_overlap_zone_name=non_overlap_zone_name_cls,
    )

