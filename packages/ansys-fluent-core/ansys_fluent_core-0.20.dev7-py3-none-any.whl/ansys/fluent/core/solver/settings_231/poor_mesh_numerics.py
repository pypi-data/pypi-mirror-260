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

from .set_1 import set as set_cls
from .list_properties_2 import list_properties as list_properties_cls
class poor_mesh_numerics(Group):
    """
    'poor_mesh_numerics' child.
    """

    fluent_name = "poor-mesh-numerics"

    child_names = \
        ['set']

    command_names = \
        ['list_properties']

    _child_classes = dict(
        set=set_cls,
        list_properties=list_properties_cls,
    )

