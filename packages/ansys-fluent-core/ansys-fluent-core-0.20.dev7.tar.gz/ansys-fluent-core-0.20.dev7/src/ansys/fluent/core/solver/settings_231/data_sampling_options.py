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

from .remove_dataset import remove_dataset as remove_dataset_cls
from .list_datasets import list_datasets as list_datasets_cls
class data_sampling_options(Group):
    """
    Data sampling options for statistics.
    """

    fluent_name = "data-sampling-options"

    command_names = \
        ['remove_dataset', 'list_datasets']

    _child_classes = dict(
        remove_dataset=remove_dataset_cls,
        list_datasets=list_datasets_cls,
    )

