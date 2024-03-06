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

from .principal_axes import principal_axes as principal_axes_cls
from .principal_values import principal_values as principal_values_cls
from .conductivity import conductivity as conductivity_cls
class principal_axes_values(Group):
    """
    'principal_axes_values' child.
    """

    fluent_name = "principal-axes-values"

    child_names = \
        ['principal_axes', 'principal_values', 'conductivity']

    _child_classes = dict(
        principal_axes=principal_axes_cls,
        principal_values=principal_values_cls,
        conductivity=conductivity_cls,
    )

