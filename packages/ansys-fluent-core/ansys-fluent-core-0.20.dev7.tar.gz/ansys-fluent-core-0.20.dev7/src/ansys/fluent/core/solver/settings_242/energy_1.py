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

from .phasic_wall_heat_flux_form import phasic_wall_heat_flux_form as phasic_wall_heat_flux_form_cls
class energy(Group):
    """
    Multiphase energy options menu.
    """

    fluent_name = "energy"

    child_names = \
        ['phasic_wall_heat_flux_form']

    _child_classes = dict(
        phasic_wall_heat_flux_form=phasic_wall_heat_flux_form_cls,
    )

