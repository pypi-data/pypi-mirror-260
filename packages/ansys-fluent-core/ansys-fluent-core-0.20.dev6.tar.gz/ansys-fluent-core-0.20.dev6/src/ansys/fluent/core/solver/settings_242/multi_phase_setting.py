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

from .enable_18 import enable as enable_cls
from .options_8 import options as options_cls
class multi_phase_setting(Group):
    """
    Set hybrid NITA for multi-phase flow.
    """

    fluent_name = "multi-phase-setting"

    child_names = \
        ['enable', 'options']

    _child_classes = dict(
        enable=enable_cls,
        options=options_cls,
    )

