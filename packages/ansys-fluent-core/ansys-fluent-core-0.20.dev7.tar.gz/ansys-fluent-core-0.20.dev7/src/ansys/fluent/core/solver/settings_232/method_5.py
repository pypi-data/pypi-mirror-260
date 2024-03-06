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

from .partition_method import partition_method as partition_method_cls
from .count import count as count_cls
class method(Command):
    """
    Partition the domain.
    
    Parameters
    ----------
        partition_method : str
            'partition_method' child.
        count : int
            'count' child.
    
    """

    fluent_name = "method"

    argument_names = \
        ['partition_method', 'count']

    _child_classes = dict(
        partition_method=partition_method_cls,
        count=count_cls,
    )

