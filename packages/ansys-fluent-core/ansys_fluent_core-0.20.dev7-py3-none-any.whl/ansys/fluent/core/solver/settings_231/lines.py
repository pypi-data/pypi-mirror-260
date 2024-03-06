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

from .lines_child import lines_child

class lines(ListObject[lines_child]):
    """
    'lines' child.
    """

    fluent_name = "lines"

    child_object_type: lines_child = lines_child
    """
    child_object_type of lines.
    """
