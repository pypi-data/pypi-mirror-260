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

class cell_zones(StringList, _HasAllowedValuesMixin):
    """
    Set cell zones to be used for marking adaption. An empty list implies that all zones are considered for adaption.
    """

    fluent_name = "cell-zones"

