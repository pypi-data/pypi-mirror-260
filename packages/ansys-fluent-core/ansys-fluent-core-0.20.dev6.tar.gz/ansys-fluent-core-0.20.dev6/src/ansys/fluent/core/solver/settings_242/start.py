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

from .session_name import session_name as session_name_cls
from .port import port as port_cls
from .port_span import port_span as port_span_cls
from .job_service_url import job_service_url as job_service_url_cls
class start(Command):
    """
    Start the web server.
    
    Parameters
    ----------
        session_name : str
            Name for the web server.
        port : int
            Listening port for the web server.
        port_span : int
            Number of ports to try starting from given 'port' for the web server.
        job_service_url : str
            Job service URL to register Fluent.
    
    """

    fluent_name = "start"

    argument_names = \
        ['session_name', 'port', 'port_span', 'job_service_url']

    _child_classes = dict(
        session_name=session_name_cls,
        port=port_cls,
        port_span=port_span_cls,
        job_service_url=job_service_url_cls,
    )

