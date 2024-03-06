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

from .joule_heat import joule_heat as joule_heat_cls
from .reaction_heat_1 import reaction_heat as reaction_heat_cls
from .electrochemistry_1 import electrochemistry as electrochemistry_cls
from .butlervolmer import butlervolmer as butlervolmer_cls
from .multidiff import multidiff as multidiff_cls
from .anisotropic import anisotropic as anisotropic_cls
from .pconductivity import pconductivity as pconductivity_cls
from .halfcell import halfcell as halfcell_cls
from .particlemodel import particlemodel as particlemodel_cls
from .liquid_phase import liquid_phase as liquid_phase_cls
from .liquid_pressure import liquid_pressure as liquid_pressure_cls
from .liquid_in_channel import liquid_in_channel as liquid_in_channel_cls
from .dynamic_head import dynamic_head as dynamic_head_cls
from .knudsen_diffusion import knudsen_diffusion as knudsen_diffusion_cls
from .temp_jref import temp_jref as temp_jref_cls
from .n2_crossover import n2_crossover as n2_crossover_cls
from .ice_phase import ice_phase as ice_phase_cls
from .dissovled_urf import dissovled_urf as dissovled_urf_cls
from .osmotic_urf import osmotic_urf as osmotic_urf_cls
from .phasechange_urf import phasechange_urf as phasechange_urf_cls
from .liquidremoval_urf import liquidremoval_urf as liquidremoval_urf_cls
from .auto_amg import auto_amg as auto_amg_cls
from .wdiff_model import wdiff_model as wdiff_model_cls
from .bc_type_1 import bc_type as bc_type_cls
from .tot_voltage import tot_voltage as tot_voltage_cls
from .tot_current import tot_current as tot_current_cls
class options(Group):
    """
    Model options.
    """

    fluent_name = "options"

    child_names = \
        ['joule_heat', 'reaction_heat', 'electrochemistry', 'butlervolmer',
         'multidiff', 'anisotropic', 'pconductivity', 'halfcell',
         'particlemodel', 'liquid_phase', 'liquid_pressure',
         'liquid_in_channel', 'dynamic_head', 'knudsen_diffusion',
         'temp_jref', 'n2_crossover', 'ice_phase', 'dissovled_urf',
         'osmotic_urf', 'phasechange_urf', 'liquidremoval_urf', 'auto_amg',
         'wdiff_model', 'bc_type', 'tot_voltage', 'tot_current']

    _child_classes = dict(
        joule_heat=joule_heat_cls,
        reaction_heat=reaction_heat_cls,
        electrochemistry=electrochemistry_cls,
        butlervolmer=butlervolmer_cls,
        multidiff=multidiff_cls,
        anisotropic=anisotropic_cls,
        pconductivity=pconductivity_cls,
        halfcell=halfcell_cls,
        particlemodel=particlemodel_cls,
        liquid_phase=liquid_phase_cls,
        liquid_pressure=liquid_pressure_cls,
        liquid_in_channel=liquid_in_channel_cls,
        dynamic_head=dynamic_head_cls,
        knudsen_diffusion=knudsen_diffusion_cls,
        temp_jref=temp_jref_cls,
        n2_crossover=n2_crossover_cls,
        ice_phase=ice_phase_cls,
        dissovled_urf=dissovled_urf_cls,
        osmotic_urf=osmotic_urf_cls,
        phasechange_urf=phasechange_urf_cls,
        liquidremoval_urf=liquidremoval_urf_cls,
        auto_amg=auto_amg_cls,
        wdiff_model=wdiff_model_cls,
        bc_type=bc_type_cls,
        tot_voltage=tot_voltage_cls,
        tot_current=tot_current_cls,
    )

