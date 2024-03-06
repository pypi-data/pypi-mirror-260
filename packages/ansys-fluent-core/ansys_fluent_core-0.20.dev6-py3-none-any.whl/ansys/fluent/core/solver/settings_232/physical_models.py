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

from .particle_drag import particle_drag as particle_drag_cls
from .particle_rotation import particle_rotation as particle_rotation_cls
from .heat_exchange import heat_exchange as heat_exchange_cls
from .custom_laws import custom_laws as custom_laws_cls
from .turbulent_dispersion import turbulent_dispersion as turbulent_dispersion_cls
from .droplet_breakup import droplet_breakup as droplet_breakup_cls
class physical_models(Group):
    """
    'physical_models' child.
    """

    fluent_name = "physical-models"

    child_names = \
        ['particle_drag', 'particle_rotation', 'heat_exchange', 'custom_laws',
         'turbulent_dispersion', 'droplet_breakup']

    _child_classes = dict(
        particle_drag=particle_drag_cls,
        particle_rotation=particle_rotation_cls,
        heat_exchange=heat_exchange_cls,
        custom_laws=custom_laws_cls,
        turbulent_dispersion=turbulent_dispersion_cls,
        droplet_breakup=droplet_breakup_cls,
    )

