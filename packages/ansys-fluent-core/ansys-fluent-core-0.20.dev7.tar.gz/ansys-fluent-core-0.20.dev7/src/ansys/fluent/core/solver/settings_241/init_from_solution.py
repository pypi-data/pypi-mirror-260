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

from .option_12 import option as option_cls
from .init_from_data_file import init_from_data_file as init_from_data_file_cls
class init_from_solution(Group):
    """
    Choose how to initialize if no solution data exists.
    """

    fluent_name = "init-from-solution"

    child_names = \
        ['option', 'init_from_data_file']

    _child_classes = dict(
        option=option_cls,
        init_from_data_file=init_from_data_file_cls,
    )

