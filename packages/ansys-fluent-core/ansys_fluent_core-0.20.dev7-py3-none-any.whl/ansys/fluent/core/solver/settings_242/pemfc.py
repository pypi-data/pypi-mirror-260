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

from .enabled_28 import enabled as enabled_cls
from .options_6 import options as options_cls
from .parameters_1 import parameters as parameters_cls
from .anode_1 import anode as anode_cls
from .membrane import membrane as membrane_cls
from .cathode_1 import cathode as cathode_cls
from .electrical_tab import electrical_tab as electrical_tab_cls
from .advanced_1 import advanced as advanced_cls
from .report_1 import report as report_cls
class pemfc(Group):
    """
    Enter PEMFC model settings.
    """

    fluent_name = "pemfc"

    child_names = \
        ['enabled', 'options', 'parameters', 'anode', 'membrane', 'cathode',
         'electrical_tab', 'advanced', 'report']

    _child_classes = dict(
        enabled=enabled_cls,
        options=options_cls,
        parameters=parameters_cls,
        anode=anode_cls,
        membrane=membrane_cls,
        cathode=cathode_cls,
        electrical_tab=electrical_tab_cls,
        advanced=advanced_cls,
        report=report_cls,
    )

