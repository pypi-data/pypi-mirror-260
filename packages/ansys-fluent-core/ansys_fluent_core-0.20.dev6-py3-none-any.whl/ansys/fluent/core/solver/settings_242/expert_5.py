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

from .reactions_2 import reactions as reactions_cls
from .reaction_source_term_relaxation_factor import reaction_source_term_relaxation_factor as reaction_source_term_relaxation_factor_cls
from .numerics_pbns import numerics_pbns as numerics_pbns_cls
from .numerics_dbns import numerics_dbns as numerics_dbns_cls
class expert(Group):
    """
    Enter expert menu.
    """

    fluent_name = "expert"

    child_names = \
        ['reactions', 'reaction_source_term_relaxation_factor',
         'numerics_pbns', 'numerics_dbns']

    _child_classes = dict(
        reactions=reactions_cls,
        reaction_source_term_relaxation_factor=reaction_source_term_relaxation_factor_cls,
        numerics_pbns=numerics_pbns_cls,
        numerics_dbns=numerics_dbns_cls,
    )

