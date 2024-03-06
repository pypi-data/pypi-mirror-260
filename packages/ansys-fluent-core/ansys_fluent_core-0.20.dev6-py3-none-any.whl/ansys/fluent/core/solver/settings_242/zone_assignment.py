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

from .positive_electrode_zone import positive_electrode_zone as positive_electrode_zone_cls
from .electrolyte_zone import electrolyte_zone as electrolyte_zone_cls
from .negative_electrode_zone import negative_electrode_zone as negative_electrode_zone_cls
class zone_assignment(Group):
    """
    Zone assignment.
    """

    fluent_name = "zone-assignment"

    child_names = \
        ['positive_electrode_zone', 'electrolyte_zone',
         'negative_electrode_zone']

    _child_classes = dict(
        positive_electrode_zone=positive_electrode_zone_cls,
        electrolyte_zone=electrolyte_zone_cls,
        negative_electrode_zone=negative_electrode_zone_cls,
    )

