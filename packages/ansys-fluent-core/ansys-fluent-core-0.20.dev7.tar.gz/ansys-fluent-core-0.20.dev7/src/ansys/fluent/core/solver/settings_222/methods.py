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

from .pressure_velocity_coupling_controls import pressure_velocity_coupling_controls as pressure_velocity_coupling_controls_cls
from .pressure_velocity_coupling_method import pressure_velocity_coupling_method as pressure_velocity_coupling_method_cls
from .gradient_controls import gradient_controls as gradient_controls_cls
from .specify_gradient_method import specify_gradient_method as specify_gradient_method_cls
class methods(Group):
    """
    'methods' child.
    """

    fluent_name = "methods"

    child_names = \
        ['pressure_velocity_coupling_controls',
         'pressure_velocity_coupling_method', 'gradient_controls',
         'specify_gradient_method']

    _child_classes = dict(
        pressure_velocity_coupling_controls=pressure_velocity_coupling_controls_cls,
        pressure_velocity_coupling_method=pressure_velocity_coupling_method_cls,
        gradient_controls=gradient_controls_cls,
        specify_gradient_method=specify_gradient_method_cls,
    )

