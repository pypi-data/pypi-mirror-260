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

from .energy_source_active_1 import energy_source_active as energy_source_active_cls
from .tab_elec_current_1 import tab_elec_current as tab_elec_current_cls
class fmu_model_settings(Group):
    """
    FMU-coupling solution method settings.
    """

    fluent_name = "fmu-model-settings"

    child_names = \
        ['energy_source_active', 'tab_elec_current']

    _child_classes = dict(
        energy_source_active=energy_source_active_cls,
        tab_elec_current=tab_elec_current_cls,
    )

