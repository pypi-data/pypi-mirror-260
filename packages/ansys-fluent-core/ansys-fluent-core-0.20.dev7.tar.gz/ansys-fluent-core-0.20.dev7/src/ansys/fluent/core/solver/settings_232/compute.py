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

from .from_zone_type import from_zone_type as from_zone_type_cls
from .from_zone_name import from_zone_name as from_zone_name_cls
from .phase_25 import phase as phase_cls
class compute(Command):
    """
    'compute' command.
    
    Parameters
    ----------
        from_zone_type : str
            'from_zone_type' child.
        from_zone_name : str
            'from_zone_name' child.
        phase : str
            'phase' child.
    
    """

    fluent_name = "compute"

    argument_names = \
        ['from_zone_type', 'from_zone_name', 'phase']

    _child_classes = dict(
        from_zone_type=from_zone_type_cls,
        from_zone_name=from_zone_name_cls,
        phase=phase_cls,
    )

