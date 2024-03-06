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

from .file_partition_method import file_partition_method as file_partition_method_cls
class use_case_file_method(Command):
    """
    Enable the use-case-file method for auto partitioning.
    
    Parameters
    ----------
        file_partition_method : bool
            'file_partition_method' child.
    
    """

    fluent_name = "use-case-file-method"

    argument_names = \
        ['file_partition_method']

    _child_classes = dict(
        file_partition_method=file_partition_method_cls,
    )

