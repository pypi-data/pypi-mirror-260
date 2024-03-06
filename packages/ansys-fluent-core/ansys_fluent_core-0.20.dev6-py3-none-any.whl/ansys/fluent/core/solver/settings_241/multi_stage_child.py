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

from .coefficient import coefficient as coefficient_cls
from .update_dissipation import update_dissipation as update_dissipation_cls
from .update_viscous import update_viscous as update_viscous_cls
class multi_stage_child(Group):
    """
    'child_object_type' of multi_stage.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'update_dissipation', 'update_viscous']

    _child_classes = dict(
        coefficient=coefficient_cls,
        update_dissipation=update_dissipation_cls,
        update_viscous=update_viscous_cls,
    )

