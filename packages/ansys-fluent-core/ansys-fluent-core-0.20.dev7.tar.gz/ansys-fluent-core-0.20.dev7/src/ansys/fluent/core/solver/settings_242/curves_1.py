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

from .lines import lines as lines_cls
from .markers import markers as markers_cls
class curves(Group):
    """
    Choose line, marker style and color for Curves.
    """

    fluent_name = "curves"

    child_names = \
        ['lines', 'markers']

    _child_classes = dict(
        lines=lines_cls,
        markers=markers_cls,
    )

