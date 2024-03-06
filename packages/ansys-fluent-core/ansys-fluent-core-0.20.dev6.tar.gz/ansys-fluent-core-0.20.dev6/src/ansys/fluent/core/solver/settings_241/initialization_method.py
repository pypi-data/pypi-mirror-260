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

from .init_from_data_file import init_from_data_file as init_from_data_file_cls
from .init_from_solution import init_from_solution as init_from_solution_cls
class initialization_method(Group):
    """
    'initialization_method' child.
    """

    fluent_name = "initialization-method"

    child_names = \
        ['init_from_data_file', 'init_from_solution']

    _child_classes = dict(
        init_from_data_file=init_from_data_file_cls,
        init_from_solution=init_from_solution_cls,
    )

