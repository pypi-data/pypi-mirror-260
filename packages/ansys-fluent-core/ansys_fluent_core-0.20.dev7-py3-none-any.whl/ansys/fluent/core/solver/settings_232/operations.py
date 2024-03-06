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

from .coarsen import coarsen as coarsen_cls
from .refine import refine as refine_cls
from .swap import swap as swap_cls
from .move import move as move_cls
class operations(Group):
    """
    Enter the anisotropic adaption operations menu.
    """

    fluent_name = "operations"

    child_names = \
        ['coarsen', 'refine', 'swap', 'move']

    _child_classes = dict(
        coarsen=coarsen_cls,
        refine=refine_cls,
        swap=swap_cls,
        move=move_cls,
    )

