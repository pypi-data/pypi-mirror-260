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

from .zone_name_4 import zone_name as zone_name_cls
from .shadow_zone_name import shadow_zone_name as shadow_zone_name_cls
from .rotate_periodic import rotate_periodic as rotate_periodic_cls
from .create import create as create_cls
from .auto_translation import auto_translation as auto_translation_cls
from .direction import direction as direction_cls
class make_periodic(Command):
    """
    Attempt to establish conformal periodic face zone connectivity.
    
    Parameters
    ----------
        zone_name : str
            Enter id/name of zone to convert to periodic.
        shadow_zone_name : str
            Enter id/name of zone to convert to shadow.
        rotate_periodic : bool
            'rotate_periodic' child.
        create : bool
            'create' child.
        auto_translation : bool
            'auto_translation' child.
        direction : typing.List[real]
            'direction' child.
    
    """

    fluent_name = "make-periodic"

    argument_names = \
        ['zone_name', 'shadow_zone_name', 'rotate_periodic', 'create',
         'auto_translation', 'direction']

    _child_classes = dict(
        zone_name=zone_name_cls,
        shadow_zone_name=shadow_zone_name_cls,
        rotate_periodic=rotate_periodic_cls,
        create=create_cls,
        auto_translation=auto_translation_cls,
        direction=direction_cls,
    )

