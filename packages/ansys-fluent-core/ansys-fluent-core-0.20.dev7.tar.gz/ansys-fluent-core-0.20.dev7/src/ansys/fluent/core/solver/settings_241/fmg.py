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
from .viscous_terms import viscous_terms as viscous_terms_cls
from .species_reactions import species_reactions as species_reactions_cls
from .turbulent_viscosity_ratio_3 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .fmg_initialize import fmg_initialize as fmg_initialize_cls
from .customize import customize as customize_cls
from .reset_to_defaults import reset_to_defaults as reset_to_defaults_cls
class fmg(Group):
    """
    Enter the set full-multigrid for initialization menu.
    """

    fluent_name = "fmg"

    child_names = \
        ['fmg_courant_number', 'enable_fmg_verbose', 'viscous_terms',
         'species_reactions', 'turbulent_viscosity_ratio']

    command_names = \
        ['fmg_initialize', 'customize', 'reset_to_defaults']

    _child_classes = dict(
        fmg_courant_number=fmg_courant_number_cls,
        enable_fmg_verbose=enable_fmg_verbose_cls,
        viscous_terms=viscous_terms_cls,
        species_reactions=species_reactions_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
        fmg_initialize=fmg_initialize_cls,
        customize=customize_cls,
        reset_to_defaults=reset_to_defaults_cls,
    )

