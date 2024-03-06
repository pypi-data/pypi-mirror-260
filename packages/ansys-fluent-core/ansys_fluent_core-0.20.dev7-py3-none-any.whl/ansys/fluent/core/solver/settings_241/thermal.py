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

from .t0 import t0 as t0_cls
class thermal(Group):
    """
    Help not available.
    """

    fluent_name = "thermal"

    child_names = \
        ['t0']

    _child_classes = dict(
        t0=t0_cls,
    )

