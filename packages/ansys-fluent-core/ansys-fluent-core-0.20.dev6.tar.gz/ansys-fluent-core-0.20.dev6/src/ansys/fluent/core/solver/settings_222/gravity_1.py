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

from .gravity import gravity as gravity_cls
from .components import components as components_cls
class gravity(Group):
    """
    'gravity' child.
    """

    fluent_name = "gravity"

    child_names = \
        ['gravity', 'components']

    _child_classes = dict(
        gravity=gravity_cls,
        components=components_cls,
    )

