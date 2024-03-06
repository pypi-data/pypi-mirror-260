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

from .print_histogram import print_histogram as print_histogram_cls
from .write_histogram import write_histogram as write_histogram_cls
class print_write_histogram(Group):
    """
    'print_write_histogram' child.
    """

    fluent_name = "print-write-histogram"

    command_names = \
        ['print_histogram', 'write_histogram']

    _child_classes = dict(
        print_histogram=print_histogram_cls,
        write_histogram=write_histogram_cls,
    )

