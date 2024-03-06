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
from .echemistry import echemistry as echemistry_cls
from .battery import battery as battery_cls
from .system_coupling import system_coupling as system_coupling_cls
from .sofc import sofc as sofc_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['multiphase', 'energy', 'viscous', 'radiation', 'species',
         'discrete_phase', 'virtual_blade_model', 'optics', 'structure',
         'ablation', 'echemistry', 'battery', 'system_coupling', 'sofc']

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
        echemistry=echemistry_cls,
        battery=battery_cls,
        system_coupling=system_coupling_cls,
        sofc=sofc_cls,
    )

