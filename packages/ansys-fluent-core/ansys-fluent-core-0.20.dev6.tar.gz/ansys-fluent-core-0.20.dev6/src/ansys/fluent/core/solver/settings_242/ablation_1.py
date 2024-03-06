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

from .ablation_select_model import ablation_select_model as ablation_select_model_cls
from .ablation_vielle_a import ablation_vielle_a as ablation_vielle_a_cls
from .ablation_vielle_n import ablation_vielle_n as ablation_vielle_n_cls
from .ablation_flux import ablation_flux as ablation_flux_cls
from .ablation_surfacerxn_density import ablation_surfacerxn_density as ablation_surfacerxn_density_cls
from .ablation_species_mf import ablation_species_mf as ablation_species_mf_cls
class ablation(Group):
    """
    Help not available.
    """

    fluent_name = "ablation"

    child_names = \
        ['ablation_select_model', 'ablation_vielle_a', 'ablation_vielle_n',
         'ablation_flux', 'ablation_surfacerxn_density',
         'ablation_species_mf']

    _child_classes = dict(
        ablation_select_model=ablation_select_model_cls,
        ablation_vielle_a=ablation_vielle_a_cls,
        ablation_vielle_n=ablation_vielle_n_cls,
        ablation_flux=ablation_flux_cls,
        ablation_surfacerxn_density=ablation_surfacerxn_density_cls,
        ablation_species_mf=ablation_species_mf_cls,
    )

