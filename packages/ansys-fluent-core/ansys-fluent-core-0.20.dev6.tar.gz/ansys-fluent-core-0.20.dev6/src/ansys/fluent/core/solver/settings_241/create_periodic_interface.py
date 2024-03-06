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

from .periodic_method import periodic_method as periodic_method_cls
from .interface_name import interface_name as interface_name_cls
from .zone_name_4 import zone_name as zone_name_cls
from .shadow_zone_name import shadow_zone_name as shadow_zone_name_cls
from .rotate_periodic import rotate_periodic as rotate_periodic_cls
from .new_axis import new_axis as new_axis_cls
from .origin import origin as origin_cls
from .new_direction import new_direction as new_direction_cls
from .direction import direction as direction_cls
from .auto_angle import auto_angle as auto_angle_cls
from .rotation_angle import rotation_angle as rotation_angle_cls
from .auto_translation import auto_translation as auto_translation_cls
from .translation import translation as translation_cls
from .create_periodic import create_periodic as create_periodic_cls
from .auto_offset import auto_offset as auto_offset_cls
from .nonconformal_angle import nonconformal_angle as nonconformal_angle_cls
from .nonconformal_translation import nonconformal_translation as nonconformal_translation_cls
from .create_matching import create_matching as create_matching_cls
from .nonconformal_create_periodic import nonconformal_create_periodic as nonconformal_create_periodic_cls
class create_periodic_interface(Command):
    """
    Create a conformal or non-conformal periodic interface.
    
    Parameters
    ----------
        periodic_method : str
            Enter method.
        interface_name : str
            Enter a name for this periodic interface.
        zone_name : str
            Enter id/name of zone to convert to periodic.
        shadow_zone_name : str
            Enter id/name of zone to convert to shadow.
        rotate_periodic : bool
            'rotate_periodic' child.
        new_axis : bool
            'new_axis' child.
        origin : typing.List[real]
            'origin' child.
        new_direction : bool
            'new_direction' child.
        direction : typing.List[real]
            'direction' child.
        auto_angle : bool
            'auto_angle' child.
        rotation_angle : real
            'rotation_angle' child.
        auto_translation : bool
            'auto_translation' child.
        translation : typing.List[real]
            'translation' child.
        create_periodic : bool
            'create_periodic' child.
        auto_offset : bool
            'auto_offset' child.
        nonconformal_angle : real
            'nonconformal_angle' child.
        nonconformal_translation : typing.List[real]
            'nonconformal_translation' child.
        create_matching : bool
            'create_matching' child.
        nonconformal_create_periodic : bool
            'nonconformal_create_periodic' child.
    
    """

    fluent_name = "create-periodic-interface"

    argument_names = \
        ['periodic_method', 'interface_name', 'zone_name', 'shadow_zone_name',
         'rotate_periodic', 'new_axis', 'origin', 'new_direction',
         'direction', 'auto_angle', 'rotation_angle', 'auto_translation',
         'translation', 'create_periodic', 'auto_offset',
         'nonconformal_angle', 'nonconformal_translation', 'create_matching',
         'nonconformal_create_periodic']

    _child_classes = dict(
        periodic_method=periodic_method_cls,
        interface_name=interface_name_cls,
        zone_name=zone_name_cls,
        shadow_zone_name=shadow_zone_name_cls,
        rotate_periodic=rotate_periodic_cls,
        new_axis=new_axis_cls,
        origin=origin_cls,
        new_direction=new_direction_cls,
        direction=direction_cls,
        auto_angle=auto_angle_cls,
        rotation_angle=rotation_angle_cls,
        auto_translation=auto_translation_cls,
        translation=translation_cls,
        create_periodic=create_periodic_cls,
        auto_offset=auto_offset_cls,
        nonconformal_angle=nonconformal_angle_cls,
        nonconformal_translation=nonconformal_translation_cls,
        create_matching=create_matching_cls,
        nonconformal_create_periodic=nonconformal_create_periodic_cls,
    )

