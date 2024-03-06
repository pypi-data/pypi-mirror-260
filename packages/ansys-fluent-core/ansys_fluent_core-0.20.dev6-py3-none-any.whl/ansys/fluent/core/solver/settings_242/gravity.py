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

from .enable_2 import enable as enable_cls
from .components import components as components_cls
from .gravity_mrf_behavior import gravity_mrf_behavior as gravity_mrf_behavior_cls
class gravity(Group):
    """
    'gravity' child.
    """

    fluent_name = "gravity"

    child_names = \
        ['enable', 'components', 'gravity_mrf_behavior']

    _child_classes = dict(
        enable=enable_cls,
        components=components_cls,
        gravity_mrf_behavior=gravity_mrf_behavior_cls,
    )

