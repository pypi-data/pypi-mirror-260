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

from .method_12 import method as method_cls
from .smoothness import smoothness as smoothness_cls
class surface_shape_sensitivity(Group):
    """
    'surface_shape_sensitivity' child.
    """

    fluent_name = "surface-shape-sensitivity"

    child_names = \
        ['method', 'smoothness']

    _child_classes = dict(
        method=method_cls,
        smoothness=smoothness_cls,
    )

