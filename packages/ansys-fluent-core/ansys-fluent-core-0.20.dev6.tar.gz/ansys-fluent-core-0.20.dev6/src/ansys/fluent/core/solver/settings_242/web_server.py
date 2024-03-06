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

from .start import start as start_cls
from .stop import stop as stop_cls
from .print_server_info import print_server_info as print_server_info_cls
from .get_server_info import get_server_info as get_server_info_cls
class web_server(Group):
    """
    REST and WebSocket based web server.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop', 'print_server_info']

    query_names = \
        ['get_server_info']

    _child_classes = dict(
        start=start_cls,
        stop=stop_cls,
        print_server_info=print_server_info_cls,
        get_server_info=get_server_info_cls,
    )

