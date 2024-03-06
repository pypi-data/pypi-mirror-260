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

from .delete_3 import delete as delete_cls
from .overlapping_percentage_threshold import overlapping_percentage_threshold as overlapping_percentage_threshold_cls
class delete_interfaces_with_small_overlap(Command):
    """
    Delete mesh interfaces that have an area percentage under a specified value.
    
    Parameters
    ----------
        delete : bool
            'delete' child.
        overlapping_percentage_threshold : real
            'overlapping_percentage_threshold' child.
    
    """

    fluent_name = "delete-interfaces-with-small-overlap"

    argument_names = \
        ['delete', 'overlapping_percentage_threshold']

    _child_classes = dict(
        delete=delete_cls,
        overlapping_percentage_threshold=overlapping_percentage_threshold_cls,
    )

