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

from .host_file import host_file as host_file_cls
class load_hosts(Command):
    """
    Read a hosts file.
    
    Parameters
    ----------
        host_file : str
            'host_file' child.
    
    """

    fluent_name = "load-hosts"

    argument_names = \
        ['host_file']

    _child_classes = dict(
        host_file=host_file_cls,
    )

