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

from .setup_reduction import setup_reduction as setup_reduction_cls
from .pick_sample_to_reduce import pick_sample_to_reduce as pick_sample_to_reduce_cls
from .reduce_picked_sample import reduce_picked_sample as reduce_picked_sample_cls
class reduction(Group):
    """
    'reduction' child.
    """

    fluent_name = "reduction"

    child_names = \
        ['setup_reduction']

    command_names = \
        ['pick_sample_to_reduce', 'reduce_picked_sample']

    _child_classes = dict(
        setup_reduction=setup_reduction_cls,
        pick_sample_to_reduce=pick_sample_to_reduce_cls,
        reduce_picked_sample=reduce_picked_sample_cls,
    )

