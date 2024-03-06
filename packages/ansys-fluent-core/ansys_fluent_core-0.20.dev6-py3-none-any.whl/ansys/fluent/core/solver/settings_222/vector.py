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
from .vector_child import vector_child

class vector(NamedObject[vector_child], _CreatableNamedObjectMixin[vector_child]):
    """
    'vector' child.
    """

    fluent_name = "vector"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: vector_child = vector_child
    """
    child_object_type of vector.
    """
