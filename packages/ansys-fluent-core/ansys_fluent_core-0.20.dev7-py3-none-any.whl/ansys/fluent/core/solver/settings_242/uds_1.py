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

from .uds_bc import uds_bc as uds_bc_cls
from .uds import uds as uds_cls
class uds(Group):
    """
    Help not available.
    """

    fluent_name = "uds"

    child_names = \
        ['uds_bc', 'uds']

    _child_classes = dict(
        uds_bc=uds_bc_cls,
        uds=uds_cls,
    )

