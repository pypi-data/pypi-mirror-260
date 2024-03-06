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
from .type_8 import type as type_cls
from .id import id as id_cls
from .normal import normal as normal_cls
from .partition import partition as partition_cls
class automatic(Group):
    """
    'automatic' child.
    """

    fluent_name = "automatic"

    child_names = \
        ['option', 'type', 'id', 'normal', 'partition']

    _child_classes = dict(
        option=option_cls,
        type=type_cls,
        id=id_cls,
        normal=normal_cls,
        partition=partition_cls,
    )

