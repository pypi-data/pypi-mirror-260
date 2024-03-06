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

from .name import name as name_cls
from .interface_names import interface_names as interface_names_cls
from .zone_names_7 import zone_names as zone_names_cls
from .zone1 import zone1 as zone1_cls
from .zone2 import zone2 as zone2_cls
from .new_zones import new_zones as new_zones_cls
from .mapped import mapped as mapped_cls
from .enable_local_mapped_tolerance import enable_local_mapped_tolerance as enable_local_mapped_tolerance_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .local_relative_mapped_tolerance import local_relative_mapped_tolerance as local_relative_mapped_tolerance_cls
from .local_absolute_mapped_tolerance import local_absolute_mapped_tolerance as local_absolute_mapped_tolerance_cls
from .periodic_1 import periodic as periodic_cls
from .turbo import turbo as turbo_cls
from .pitch_change_types import pitch_change_types as pitch_change_types_cls
from .mixing_plane import mixing_plane as mixing_plane_cls
from .turbo_non_overlap import turbo_non_overlap as turbo_non_overlap_cls
from .coupled_1 import coupled as coupled_cls
from .matching import matching as matching_cls
from .static_1 import static as static_cls
from .ignore_diff import ignore_diff as ignore_diff_cls
class interface_child(Group):
    """
    'child_object_type' of interface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'interface_names', 'zone_names', 'zone1', 'zone2',
         'new_zones', 'mapped', 'enable_local_mapped_tolerance',
         'use_local_edge_length_factor', 'local_relative_mapped_tolerance',
         'local_absolute_mapped_tolerance', 'periodic', 'turbo',
         'pitch_change_types', 'mixing_plane', 'turbo_non_overlap', 'coupled',
         'matching', 'static', 'ignore_diff']

    _child_classes = dict(
        name=name_cls,
        interface_names=interface_names_cls,
        zone_names=zone_names_cls,
        zone1=zone1_cls,
        zone2=zone2_cls,
        new_zones=new_zones_cls,
        mapped=mapped_cls,
        enable_local_mapped_tolerance=enable_local_mapped_tolerance_cls,
        use_local_edge_length_factor=use_local_edge_length_factor_cls,
        local_relative_mapped_tolerance=local_relative_mapped_tolerance_cls,
        local_absolute_mapped_tolerance=local_absolute_mapped_tolerance_cls,
        periodic=periodic_cls,
        turbo=turbo_cls,
        pitch_change_types=pitch_change_types_cls,
        mixing_plane=mixing_plane_cls,
        turbo_non_overlap=turbo_non_overlap_cls,
        coupled=coupled_cls,
        matching=matching_cls,
        static=static_cls,
        ignore_diff=ignore_diff_cls,
    )

