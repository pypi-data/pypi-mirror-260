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

from .user_defined_functions_1 import user_defined_functions as user_defined_functions_cls
from .sort_sample_files import sort_sample_files as sort_sample_files_cls
from .sample_1 import sample as sample_cls
class sample_trajectories(Group):
    """
    'sample_trajectories' child.
    """

    fluent_name = "sample-trajectories"

    child_names = \
        ['user_defined_functions', 'sort_sample_files']

    command_names = \
        ['sample']

    _child_classes = dict(
        user_defined_functions=user_defined_functions_cls,
        sort_sample_files=sort_sample_files_cls,
        sample=sample_cls,
    )

