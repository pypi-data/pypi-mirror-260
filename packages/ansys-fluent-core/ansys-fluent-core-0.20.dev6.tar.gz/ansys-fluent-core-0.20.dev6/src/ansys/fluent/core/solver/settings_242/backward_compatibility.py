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

from .pre_24r2_mp_discretization import pre_24r2_mp_discretization as pre_24r2_mp_discretization_cls
class backward_compatibility(Group):
    """
    List of backward compatbility options for GTI.
    """

    fluent_name = "backward-compatibility"

    command_names = \
        ['pre_24r2_mp_discretization']

    _child_classes = dict(
        pre_24r2_mp_discretization=pre_24r2_mp_discretization_cls,
    )

