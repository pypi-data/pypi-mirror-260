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

from .enable_8 import enable as enable_cls
from .mode import mode as mode_cls
from .rotor import rotor as rotor_cls
from .apply import apply as apply_cls
class virtual_blade_model(Group):
    """
    Enter the vbm model menu.
    """

    fluent_name = "virtual-blade-model"

    child_names = \
        ['enable', 'mode', 'rotor']

    command_names = \
        ['apply']

    _child_classes = dict(
        enable=enable_cls,
        mode=mode_cls,
        rotor=rotor_cls,
        apply=apply_cls,
    )

