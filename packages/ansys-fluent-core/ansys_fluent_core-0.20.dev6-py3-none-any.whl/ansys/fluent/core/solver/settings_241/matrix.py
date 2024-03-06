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

from .r import r as r_cls
from .u import u as u_cls
class matrix(Group):
    """
    'matrix' child.
    """

    fluent_name = "matrix"

    child_names = \
        ['r', 'u']

    _child_classes = dict(
        r=r_cls,
        u=u_cls,
    )

