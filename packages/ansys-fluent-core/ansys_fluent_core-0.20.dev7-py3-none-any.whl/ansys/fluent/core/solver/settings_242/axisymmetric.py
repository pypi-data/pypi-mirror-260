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

from .axis_stabilization import axis_stabilization as axis_stabilization_cls
class axisymmetric(Group):
    """
    Enter axisymmetric menu.
    """

    fluent_name = "axisymmetric"

    child_names = \
        ['axis_stabilization']

    _child_classes = dict(
        axis_stabilization=axis_stabilization_cls,
    )

