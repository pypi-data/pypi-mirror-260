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
from .dissipation import dissipation as dissipation_cls
from .viscous_1 import viscous as viscous_cls
class multi_stage_child(Group):
    """
    'child_object_type' of multi_stage.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'dissipation', 'viscous']

    _child_classes = dict(
        coefficient=coefficient_cls,
        dissipation=dissipation_cls,
        viscous=viscous_cls,
    )

