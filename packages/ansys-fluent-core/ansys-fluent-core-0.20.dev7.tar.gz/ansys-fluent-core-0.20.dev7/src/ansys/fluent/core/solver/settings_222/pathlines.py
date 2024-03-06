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

from .display import display as display_cls
from .pathlines_child import pathlines_child

class pathlines(NamedObject[pathlines_child], _CreatableNamedObjectMixin[pathlines_child]):
    """
    'pathlines' child.
    """

    fluent_name = "pathlines"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: pathlines_child = pathlines_child
    """
    child_object_type of pathlines.
    """
