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

from .zone_names_3 import zone_names as zone_names_cls
from .offset import offset as offset_cls
class translate_zone(Command):
    """
    Translate nodal coordinates of input cell zones.
    
    Parameters
    ----------
        zone_names : typing.List[str]
            Translate specified cell zones.
        offset : typing.List[real]
            'offset' child.
    
    """

    fluent_name = "translate-zone"

    argument_names = \
        ['zone_names', 'offset']

    _child_classes = dict(
        zone_names=zone_names_cls,
        offset=offset_cls,
    )

