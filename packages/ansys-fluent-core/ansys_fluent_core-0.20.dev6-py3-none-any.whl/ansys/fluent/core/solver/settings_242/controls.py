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

from .numerical_damping_factor import numerical_damping_factor as numerical_damping_factor_cls
from .enhanced_strain import enhanced_strain as enhanced_strain_cls
from .unsteady_damping_rayleigh import unsteady_damping_rayleigh as unsteady_damping_rayleigh_cls
from .amg_stabilization import amg_stabilization as amg_stabilization_cls
from .max_iter import max_iter as max_iter_cls
class controls(Group):
    """
    Enter the structure controls menu.
    """

    fluent_name = "controls"

    child_names = \
        ['numerical_damping_factor', 'enhanced_strain',
         'unsteady_damping_rayleigh', 'amg_stabilization', 'max_iter']

    _child_classes = dict(
        numerical_damping_factor=numerical_damping_factor_cls,
        enhanced_strain=enhanced_strain_cls,
        unsteady_damping_rayleigh=unsteady_damping_rayleigh_cls,
        amg_stabilization=amg_stabilization_cls,
        max_iter=max_iter_cls,
    )

