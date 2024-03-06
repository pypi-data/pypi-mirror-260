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

from .sensitivity_orientation import sensitivity_orientation as sensitivity_orientation_cls
from .surface_shape_sensitivity import surface_shape_sensitivity as surface_shape_sensitivity_cls
from .reset_default import reset_default as reset_default_cls
class postprocess_options(Group):
    """
    Enter the postprocessing options menu.
    """

    fluent_name = "postprocess-options"

    child_names = \
        ['sensitivity_orientation', 'surface_shape_sensitivity']

    command_names = \
        ['reset_default']

    _child_classes = dict(
        sensitivity_orientation=sensitivity_orientation_cls,
        surface_shape_sensitivity=surface_shape_sensitivity_cls,
        reset_default=reset_default_cls,
    )

