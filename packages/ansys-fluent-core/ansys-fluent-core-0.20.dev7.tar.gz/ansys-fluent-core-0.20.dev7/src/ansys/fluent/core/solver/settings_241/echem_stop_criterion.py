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

from .echem_stop_type import echem_stop_type as echem_stop_type_cls
from .min_voltage import min_voltage as min_voltage_cls
from .max_voltage import max_voltage as max_voltage_cls
from .min_soc import min_soc as min_soc_cls
from .max_soc import max_soc as max_soc_cls
class echem_stop_criterion(Group):
    """
    'echem_stop_criterion' child.
    """

    fluent_name = "echem-stop-criterion"

    child_names = \
        ['echem_stop_type', 'min_voltage', 'max_voltage', 'min_soc',
         'max_soc']

    _child_classes = dict(
        echem_stop_type=echem_stop_type_cls,
        min_voltage=min_voltage_cls,
        max_voltage=max_voltage_cls,
        min_soc=min_soc_cls,
        max_soc=max_soc_cls,
    )

