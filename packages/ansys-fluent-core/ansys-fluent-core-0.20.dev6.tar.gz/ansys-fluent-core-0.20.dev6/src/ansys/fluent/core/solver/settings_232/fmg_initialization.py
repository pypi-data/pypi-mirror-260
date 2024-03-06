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

from .fmg_courant_number import fmg_courant_number as fmg_courant_number_cls
from .enable_fmg_verbose import enable_fmg_verbose as enable_fmg_verbose_cls
from .customize_fmg_initialization import customize_fmg_initialization as customize_fmg_initialization_cls
class fmg_initialization(Group):
    """
    Enter the set full-multigrid for initialization menu.
    """

    fluent_name = "fmg-initialization"

    child_names = \
        ['fmg_courant_number', 'enable_fmg_verbose']

    command_names = \
        ['customize_fmg_initialization']

    _child_classes = dict(
        fmg_courant_number=fmg_courant_number_cls,
        enable_fmg_verbose=enable_fmg_verbose_cls,
        customize_fmg_initialization=customize_fmg_initialization_cls,
    )

