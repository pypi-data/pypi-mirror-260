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

from .case_file import case_file as case_file_cls
from .across_zones import across_zones as across_zones_cls
from .method_2 import method as method_cls
from .load_vector import load_vector as load_vector_cls
from .pre_test import pre_test as pre_test_cls
class auto(Group):
    """
    Enter the menu to set auto partition parameters.
    """

    fluent_name = "auto"

    child_names = \
        ['case_file', 'across_zones', 'method', 'load_vector', 'pre_test']

    _child_classes = dict(
        case_file=case_file_cls,
        across_zones=across_zones_cls,
        method=method_cls,
        load_vector=load_vector_cls,
        pre_test=pre_test_cls,
    )

