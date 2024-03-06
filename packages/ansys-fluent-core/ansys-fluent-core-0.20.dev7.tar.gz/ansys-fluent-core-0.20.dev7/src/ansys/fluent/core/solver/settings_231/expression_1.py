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

from .expression_child import expression_child

class expression(NamedObject[expression_child], _CreatableNamedObjectMixin[expression_child]):
    """
    'expression' child.
    """

    fluent_name = "expression"

    child_object_type: expression_child = expression_child
    """
    child_object_type of expression.
    """
