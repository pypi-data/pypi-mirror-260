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

from .process_count import process_count as process_count_cls
from .host_name import host_name as host_name_cls
class helper_session_setup(Group):
    """
    Setup helper session for multidomain conjugate heat transfer.
    """

    fluent_name = "helper-session-setup"

    child_names = \
        ['process_count', 'host_name']

    _child_classes = dict(
        process_count=process_count_cls,
        host_name=host_name_cls,
    )

