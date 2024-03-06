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

from .zone_names_4 import zone_names as zone_names_cls
class create_multiple_zone_surfaces(Command):
    """
    'create_multiple_zone_surfaces' command.
    
    Parameters
    ----------
        zone_names : typing.List[str]
            Enter zone name list.
    
    """

    fluent_name = "create-multiple-zone-surfaces"

    argument_names = \
        ['zone_names']

    _child_classes = dict(
        zone_names=zone_names_cls,
    )

