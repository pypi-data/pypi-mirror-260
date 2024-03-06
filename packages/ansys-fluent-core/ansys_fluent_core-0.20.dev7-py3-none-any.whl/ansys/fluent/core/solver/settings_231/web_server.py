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
class web_server(Group):
    """
    'web_server' child.
    """

    fluent_name = "web-server"

    command_names = \
        ['start', 'stop']

    _child_classes = dict(
        start=start_cls,
        stop=stop_cls,
    )

