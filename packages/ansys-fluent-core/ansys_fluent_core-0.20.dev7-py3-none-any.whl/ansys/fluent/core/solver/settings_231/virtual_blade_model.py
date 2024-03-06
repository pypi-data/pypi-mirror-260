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

from .enable_4 import enable as enable_cls
from .mode import mode as mode_cls
from .disk import disk as disk_cls
class virtual_blade_model(Group):
    """
    Enter the vbm model menu.
    """

    fluent_name = "virtual-blade-model"

    child_names = \
        ['enable', 'mode', 'disk']

    _child_classes = dict(
        enable=enable_cls,
        mode=mode_cls,
        disk=disk_cls,
    )

