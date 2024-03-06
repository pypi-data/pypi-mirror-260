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

from .multiphase import multiphase as multiphase_cls
from .energy import energy as energy_cls
from .viscous import viscous as viscous_cls
from .radiation import radiation as radiation_cls
from .species import species as species_cls
from .discrete_phase import discrete_phase as discrete_phase_cls
from .virtual_blade_model import virtual_blade_model as virtual_blade_model_cls
from .optics import optics as optics_cls
from .structure import structure as structure_cls
from .ablation import ablation as ablation_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['multiphase', 'energy', 'viscous', 'radiation', 'species',
         'discrete_phase', 'virtual_blade_model', 'optics', 'structure',
         'ablation']

    _child_classes = dict(
        multiphase=multiphase_cls,
        energy=energy_cls,
        viscous=viscous_cls,
        radiation=radiation_cls,
        species=species_cls,
        discrete_phase=discrete_phase_cls,
        virtual_blade_model=virtual_blade_model_cls,
        optics=optics_cls,
        structure=structure_cls,
        ablation=ablation_cls,
    )

