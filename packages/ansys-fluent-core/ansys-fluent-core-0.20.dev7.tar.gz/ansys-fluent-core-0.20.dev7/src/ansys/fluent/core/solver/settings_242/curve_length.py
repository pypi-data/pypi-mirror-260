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

from .option import option as option_cls
from .default import default as default_cls
from .reverse import reverse as reverse_cls
class curve_length(Group):
    """
    'curve_length' child.
    """

    fluent_name = "curve-length"

    child_names = \
        ['option', 'default', 'reverse']

    _child_classes = dict(
        option=option_cls,
        default=default_cls,
        reverse=reverse_cls,
    )

