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

class option(String, _HasAllowedValuesMixin):
    """
    (0) basic:           name-prefix:##
    (1) name-based:      name-prefix:##:interface_name1::interface_name2
    (2) ID-based:        name-prefix:##:interface_ID1::interface-ID2
    (3) adjacency-based: name-prefix:##:cell_zone_name1::cell_zone_name2.
    """

    fluent_name = "option"

