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

from .discrete_phase import discrete_phase as discrete_phase_cls
from .energy import energy as energy_cls
from .multiphase import multiphase as multiphase_cls
from .viscous import viscous as viscous_cls
from .optics import optics as optics_cls
from .virtual_blade_model import virtual_blade_model as virtual_blade_model_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['discrete_phase', 'energy', 'multiphase', 'viscous', 'optics',
         'virtual_blade_model']

    _child_classes = dict(
        discrete_phase=discrete_phase_cls,
        energy=energy_cls,
        multiphase=multiphase_cls,
        viscous=viscous_cls,
        optics=optics_cls,
        virtual_blade_model=virtual_blade_model_cls,
    )

