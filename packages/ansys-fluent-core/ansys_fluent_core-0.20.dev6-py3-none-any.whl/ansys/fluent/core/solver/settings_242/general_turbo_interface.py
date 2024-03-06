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

from .expert_4 import expert as expert_cls
from .mixing_plane_model import mixing_plane_model as mixing_plane_model_cls
class general_turbo_interface(Group):
    """
    Enter the general turbo interface settings.
    """

    fluent_name = "general-turbo-interface"

    child_names = \
        ['expert', 'mixing_plane_model']

    _child_classes = dict(
        expert=expert_cls,
        mixing_plane_model=mixing_plane_model_cls,
    )

