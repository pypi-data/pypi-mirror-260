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

from .low_order_rhie_chow import low_order_rhie_chow as low_order_rhie_chow_cls
class rhie_chow_flux(Group):
    """
    'rhie_chow_flux' child.
    """

    fluent_name = "rhie-chow-flux"

    child_names = \
        ['low_order_rhie_chow']

    _child_classes = dict(
        low_order_rhie_chow=low_order_rhie_chow_cls,
    )

