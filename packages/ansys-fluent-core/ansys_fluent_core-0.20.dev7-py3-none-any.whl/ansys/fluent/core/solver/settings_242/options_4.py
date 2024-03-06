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

from .device_type import device_type as device_type_cls
from .mea_model import mea_model as mea_model_cls
from .source_enabled import source_enabled as source_enabled_cls
from .butlervolmer_rate import butlervolmer_rate as butlervolmer_rate_cls
from .multidiff_enabled import multidiff_enabled as multidiff_enabled_cls
from .halfcell_voltage import halfcell_voltage as halfcell_voltage_cls
from .osmotic_drag import osmotic_drag as osmotic_drag_cls
from .capillary_pressure import capillary_pressure as capillary_pressure_cls
from .reaction_heat import reaction_heat as reaction_heat_cls
from .phase_change import phase_change as phase_change_cls
from .water_content import water_content as water_content_cls
from .bc_type import bc_type as bc_type_cls
from .tot_voltage import tot_voltage as tot_voltage_cls
from .tot_current import tot_current as tot_current_cls
class options(Group):
    """
    Model options.
    """

    fluent_name = "options"

    child_names = \
        ['device_type', 'mea_model', 'source_enabled', 'butlervolmer_rate',
         'multidiff_enabled', 'halfcell_voltage', 'osmotic_drag',
         'capillary_pressure', 'reaction_heat', 'phase_change',
         'water_content', 'bc_type', 'tot_voltage', 'tot_current']

    _child_classes = dict(
        device_type=device_type_cls,
        mea_model=mea_model_cls,
        source_enabled=source_enabled_cls,
        butlervolmer_rate=butlervolmer_rate_cls,
        multidiff_enabled=multidiff_enabled_cls,
        halfcell_voltage=halfcell_voltage_cls,
        osmotic_drag=osmotic_drag_cls,
        capillary_pressure=capillary_pressure_cls,
        reaction_heat=reaction_heat_cls,
        phase_change=phase_change_cls,
        water_content=water_content_cls,
        bc_type=bc_type_cls,
        tot_voltage=tot_voltage_cls,
        tot_current=tot_current_cls,
    )

