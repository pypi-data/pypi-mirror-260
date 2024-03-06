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

from .option import option as option_cls
from .none_1 import none as none_cls
from .gradient_1 import gradient as gradient_cls
from .curvature import curvature as curvature_cls
from .hessian import hessian as hessian_cls
class derivative(Group):
    """
    'derivative' child.
    """

    fluent_name = "derivative"

    child_names = \
        ['option', 'none', 'gradient', 'curvature', 'hessian']

    _child_classes = dict(
        option=option_cls,
        none=none_cls,
        gradient=gradient_cls,
        curvature=curvature_cls,
        hessian=hessian_cls,
    )

