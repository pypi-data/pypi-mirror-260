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

from .damping_factor_1 import damping_factor as damping_factor_cls
from .damping_relaxation import damping_relaxation as damping_relaxation_cls
from .damping_order import damping_order as damping_order_cls
from .suppression import suppression as suppression_cls
from .default_2 import default as default_cls
class dissipation(Group):
    """
    Enter the dissipation method stabilization controls menu.
    """

    fluent_name = "dissipation"

    child_names = \
        ['damping_factor', 'damping_relaxation', 'damping_order',
         'suppression']

    command_names = \
        ['default']

    _child_classes = dict(
        damping_factor=damping_factor_cls,
        damping_relaxation=damping_relaxation_cls,
        damping_order=damping_order_cls,
        suppression=suppression_cls,
        default=default_cls,
    )

