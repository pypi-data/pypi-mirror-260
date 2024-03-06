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

from .number_of_partitions import number_of_partitions as number_of_partitions_cls
class combine_partition(Command):
    """
    Merge every N partitions.
    
    Parameters
    ----------
        number_of_partitions : int
            'number_of_partitions' child.
    
    """

    fluent_name = "combine-partition"

    argument_names = \
        ['number_of_partitions']

    _child_classes = dict(
        number_of_partitions=number_of_partitions_cls,
    )

