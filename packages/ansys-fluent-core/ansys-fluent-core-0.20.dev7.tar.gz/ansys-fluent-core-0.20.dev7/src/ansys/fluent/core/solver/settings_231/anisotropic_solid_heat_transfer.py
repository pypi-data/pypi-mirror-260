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

from .flux import flux as flux_cls
from .gradient import gradient as gradient_cls
class anisotropic_solid_heat_transfer(Group):
    """
    'anisotropic_solid_heat_transfer' child.
    """

    fluent_name = "anisotropic-solid-heat-transfer"

    child_names = \
        ['flux', 'gradient']

    _child_classes = dict(
        flux=flux_cls,
        gradient=gradient_cls,
    )

