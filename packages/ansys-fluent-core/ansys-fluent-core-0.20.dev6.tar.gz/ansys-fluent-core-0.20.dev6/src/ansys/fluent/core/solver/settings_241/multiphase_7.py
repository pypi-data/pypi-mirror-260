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

from .gtemp_bc import gtemp_bc as gtemp_bc_cls
from .g_temperature import g_temperature as g_temperature_cls
from .g_qflux import g_qflux as g_qflux_cls
from .wall_restitution_coeff import wall_restitution_coeff as wall_restitution_coeff_cls
from .contact_angles import contact_angles as contact_angles_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['gtemp_bc', 'g_temperature', 'g_qflux', 'wall_restitution_coeff',
         'contact_angles']

    _child_classes = dict(
        gtemp_bc=gtemp_bc_cls,
        g_temperature=g_temperature_cls,
        g_qflux=g_qflux_cls,
        wall_restitution_coeff=wall_restitution_coeff_cls,
        contact_angles=contact_angles_cls,
    )

