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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .test_data_sets_child import test_data_sets_child

class test_data_sets(ListObject[test_data_sets_child]):
    """
    Define test data sets.
    """

    fluent_name = "test-data-sets"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: test_data_sets_child = test_data_sets_child
    """
    child_object_type of test_data_sets.
    """
