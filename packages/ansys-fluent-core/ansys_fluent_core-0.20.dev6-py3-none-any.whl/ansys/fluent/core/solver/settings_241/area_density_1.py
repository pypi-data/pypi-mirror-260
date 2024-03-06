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

from .vof_min_seeding import vof_min_seeding as vof_min_seeding_cls
from .ia_grad_sym import ia_grad_sym as ia_grad_sym_cls
class area_density(Group):
    """
    Interfacial area density menu.
    """

    fluent_name = "area-density"

    child_names = \
        ['vof_min_seeding', 'ia_grad_sym']

    _child_classes = dict(
        vof_min_seeding=vof_min_seeding_cls,
        ia_grad_sym=ia_grad_sym_cls,
    )

