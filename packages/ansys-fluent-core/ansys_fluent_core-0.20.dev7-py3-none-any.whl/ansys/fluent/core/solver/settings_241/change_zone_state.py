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

from .zone_name_3 import zone_name as zone_name_cls
from .domain import domain as domain_cls
from .new_phase import new_phase as new_phase_cls
class change_zone_state(Command):
    """
    Change the realgas material state for a zone.
    
    Parameters
    ----------
        zone_name : str
            Enter a fluid zone name.
        domain : str
            'domain' child.
        new_phase : int
            'new_phase' child.
    
    """

    fluent_name = "change-zone-state"

    argument_names = \
        ['zone_name', 'domain', 'new_phase']

    _child_classes = dict(
        zone_name=zone_name_cls,
        domain=domain_cls,
        new_phase=new_phase_cls,
    )

