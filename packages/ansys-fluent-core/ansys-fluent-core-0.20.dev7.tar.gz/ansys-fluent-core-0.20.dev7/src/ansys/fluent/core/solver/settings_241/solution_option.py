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

from .joule_heat_in_passive_zone import joule_heat_in_passive_zone as joule_heat_in_passive_zone_cls
from .echem_heat_enabled import echem_heat_enabled as echem_heat_enabled_cls
from .entropic_heat import entropic_heat as entropic_heat_cls
from .current_urf import current_urf as current_urf_cls
from .voltage_correction_urf import voltage_correction_urf as voltage_correction_urf_cls
class solution_option(Group):
    """
    'solution_option' child.
    """

    fluent_name = "solution-option"

    child_names = \
        ['joule_heat_in_passive_zone', 'echem_heat_enabled', 'entropic_heat',
         'current_urf', 'voltage_correction_urf']

    _child_classes = dict(
        joule_heat_in_passive_zone=joule_heat_in_passive_zone_cls,
        echem_heat_enabled=echem_heat_enabled_cls,
        entropic_heat=entropic_heat_cls,
        current_urf=current_urf_cls,
        voltage_correction_urf=voltage_correction_urf_cls,
    )

