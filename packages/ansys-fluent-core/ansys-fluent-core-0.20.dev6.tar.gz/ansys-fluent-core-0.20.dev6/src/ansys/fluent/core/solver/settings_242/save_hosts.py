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

from .host_file_1 import host_file_1 as host_file_1_cls
class save_hosts(Command):
    """
    Write a hosts file.
    
    Parameters
    ----------
        host_file_1 : str
            'host_file' child.
    
    """

    fluent_name = "save-hosts"

    argument_names = \
        ['host_file']

    _child_classes = dict(
        host_file=host_file_1_cls,
    )

