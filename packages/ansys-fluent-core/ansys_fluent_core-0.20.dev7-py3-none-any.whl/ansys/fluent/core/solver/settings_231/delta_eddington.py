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

from .forward_scattering_factor import forward_scattering_factor as forward_scattering_factor_cls
from .asymmetry_factor import asymmetry_factor as asymmetry_factor_cls
class delta_eddington(Group):
    """
    'delta_eddington' child.
    """

    fluent_name = "delta-eddington"

    child_names = \
        ['forward_scattering_factor', 'asymmetry_factor']

    _child_classes = dict(
        forward_scattering_factor=forward_scattering_factor_cls,
        asymmetry_factor=asymmetry_factor_cls,
    )

