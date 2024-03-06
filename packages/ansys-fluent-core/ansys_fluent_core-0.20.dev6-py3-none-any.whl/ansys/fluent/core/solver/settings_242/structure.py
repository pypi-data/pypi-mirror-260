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

from .model_1 import model as model_cls
from .options_3 import options as options_cls
from .controls import controls as controls_cls
from .expert_3 import expert as expert_cls
class structure(Group):
    """
    'structure' child.
    """

    fluent_name = "structure"

    child_names = \
        ['model', 'options', 'controls', 'expert']

    _child_classes = dict(
        model=model_cls,
        options=options_cls,
        controls=controls_cls,
        expert=expert_cls,
    )

