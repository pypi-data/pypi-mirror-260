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

from .data_sets import data_sets as data_sets_cls
from .add_datasets import add_datasets as add_datasets_cls
from .list_datasets import list_datasets as list_datasets_cls
class data_sampling_options(Group):
    """
    Data sampling options for statistics.
    """

    fluent_name = "data-sampling-options"

    child_names = \
        ['data_sets']

    command_names = \
        ['add_datasets', 'list_datasets']

    _child_classes = dict(
        data_sets=data_sets_cls,
        add_datasets=add_datasets_cls,
        list_datasets=list_datasets_cls,
    )

