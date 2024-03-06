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

from .line import line as line_cls
from .line_in_file import line_in_file as line_in_file_cls
from .marker import marker as marker_cls
from .marker_in_file import marker_in_file as marker_in_file_cls
class curves_child(Group):
    """
    'child_object_type' of curves.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['line', 'line_in_file', 'marker', 'marker_in_file']

    _child_classes = dict(
        line=line_cls,
        line_in_file=line_in_file_cls,
        marker=marker_cls,
        marker_in_file=marker_in_file_cls,
    )

