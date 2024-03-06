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

from .from_zone_type_1 import from_zone_type as from_zone_type_cls
from .from_zone_name_1 import from_zone_name as from_zone_name_cls
from .phase_29 import phase as phase_cls
class compute_defaults(Command):
    """
    Compute default values from selection.
    
    Parameters
    ----------
        from_zone_type : str
            Select boundary/zone type.
        from_zone_name : str
            Selecte zone name.
        phase : str
            Select phase name.
    
    """

    fluent_name = "compute-defaults"

    argument_names = \
        ['from_zone_type', 'from_zone_name', 'phase']

    _child_classes = dict(
        from_zone_type=from_zone_type_cls,
        from_zone_name=from_zone_name_cls,
        phase=phase_cls,
    )

