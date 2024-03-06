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

from .coupling import coupling as coupling_cls
from .helper_session_setup import helper_session_setup as helper_session_setup_cls
from .helper_session import helper_session as helper_session_cls
class set(Group):
    """
    Enter the set menu for loosely coupled conjugate heat transfer.
    """

    fluent_name = "set"

    child_names = \
        ['coupling', 'helper_session_setup', 'helper_session']

    _child_classes = dict(
        coupling=coupling_cls,
        helper_session_setup=helper_session_setup_cls,
        helper_session=helper_session_cls,
    )

