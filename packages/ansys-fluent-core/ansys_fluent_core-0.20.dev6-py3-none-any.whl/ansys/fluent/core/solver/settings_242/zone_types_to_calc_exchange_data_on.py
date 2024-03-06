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

class zone_types_to_calc_exchange_data_on(String, _HasAllowedValuesMixin):
    """
    Choose whether, and for which zone types (Lagr. wall film or cell zones [for free-stream particles])
    to collect and store detailed information about DPM exchange terms on individual zones
    (for DPM summary reports).
    """

    fluent_name = "zone-types-to-calc-exchange-data-on"

