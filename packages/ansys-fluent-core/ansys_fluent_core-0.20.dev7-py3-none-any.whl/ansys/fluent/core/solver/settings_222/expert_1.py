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

from .spatial_discretization_limiter import spatial_discretization_limiter as spatial_discretization_limiter_cls
class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['spatial_discretization_limiter']

    _child_classes = dict(
        spatial_discretization_limiter=spatial_discretization_limiter_cls,
    )

