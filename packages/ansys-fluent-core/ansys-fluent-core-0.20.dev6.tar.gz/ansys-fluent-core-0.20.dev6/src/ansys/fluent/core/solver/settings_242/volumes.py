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

from .fluid_2 import fluid as fluid_cls
from .solid_2 import solid as solid_cls
class volumes(Group):
    """
    Select type of volume.
    """

    fluent_name = "volumes"

    child_names = \
        ['fluid', 'solid']

    _child_classes = dict(
        fluid=fluid_cls,
        solid=solid_cls,
    )

