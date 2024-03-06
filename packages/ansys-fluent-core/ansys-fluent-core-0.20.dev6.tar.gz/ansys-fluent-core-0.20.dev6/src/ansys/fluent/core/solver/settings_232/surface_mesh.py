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

from .delete import delete as delete_cls
from .display import display as display_cls
from .read_2 import read as read_cls
class surface_mesh(Group):
    """
    Enter the surface mesh menu.
    """

    fluent_name = "surface-mesh"

    command_names = \
        ['delete', 'display', 'read']

    _child_classes = dict(
        delete=delete_cls,
        display=display_cls,
        read=read_cls,
    )

