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

from .limiter_type import limiter_type as limiter_type_cls
from .cell_to_limiting import cell_to_limiting as cell_to_limiting_cls
from .limiter_filter import limiter_filter as limiter_filter_cls
class spatial_discretization_limiter(Group):
    """
    Enter the slope limiter set menu.
    """

    fluent_name = "spatial-discretization-limiter"

    child_names = \
        ['limiter_type', 'cell_to_limiting', 'limiter_filter']

    _child_classes = dict(
        limiter_type=limiter_type_cls,
        cell_to_limiting=cell_to_limiting_cls,
        limiter_filter=limiter_filter_cls,
    )

