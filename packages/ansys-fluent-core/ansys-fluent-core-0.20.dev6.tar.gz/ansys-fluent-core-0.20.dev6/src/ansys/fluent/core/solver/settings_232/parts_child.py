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

from .bodies import bodies as bodies_cls
from .groups import groups as groups_cls
class parts_child(Group):
    """
    'child_object_type' of parts.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['bodies', 'groups']

    _child_classes = dict(
        bodies=bodies_cls,
        groups=groups_cls,
    )

