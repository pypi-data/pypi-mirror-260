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

from .web_server import web_server as web_server_cls
class server(Group):
    """
    'server' child.
    """

    fluent_name = "server"

    child_names = \
        ['web_server']

    _child_classes = dict(
        web_server=web_server_cls,
    )

