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

from .format_type import format_type as format_type_cls
from .precision import precision as precision_cls
class number_format(Group):
    """
    Set number-formatting options.
    """

    fluent_name = "number-format"

    child_names = \
        ['format_type', 'precision']

    _child_classes = dict(
        format_type=format_type_cls,
        precision=precision_cls,
    )

