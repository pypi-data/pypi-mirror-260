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

from .model import model as model_cls
from .expert import expert as expert_cls
class translational_vibrational_energy_relaxation(Group):
    """
    Define translational-vibrational energy relaxation model.
    """

    fluent_name = "translational-vibrational-energy-relaxation"

    child_names = \
        ['model', 'expert']

    _child_classes = dict(
        model=model_cls,
        expert=expert_cls,
    )

