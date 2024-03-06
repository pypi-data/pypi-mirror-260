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

from .name_2 import name as name_cls
from .zone1 import zone1 as zone1_cls
from .zone2 import zone2 as zone2_cls
from .zone1_list import zone1_list as zone1_list_cls
from .zone2_list import zone2_list as zone2_list_cls
from .mapped import mapped as mapped_cls
from .enable_local_mapped_tolerance import enable_local_mapped_tolerance as enable_local_mapped_tolerance_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .local_relative_mapped_tolerance import local_relative_mapped_tolerance as local_relative_mapped_tolerance_cls
from .local_absolute_mapped_tolerance import local_absolute_mapped_tolerance as local_absolute_mapped_tolerance_cls
from .periodic_2 import periodic as periodic_cls
from .turbo import turbo as turbo_cls
from .turbo_choice import turbo_choice as turbo_choice_cls
from .mixing_plane import mixing_plane as mixing_plane_cls
from .turbo_non_overlap import turbo_non_overlap as turbo_non_overlap_cls
from .coupled_1 import coupled as coupled_cls
from .matching import matching as matching_cls
from .static_1 import static as static_cls
class create(Command):
    """
    Create mesh interfaces.
    
    Parameters
    ----------
        name : str
            Enter a prefix for mesh interface names.
        zone1 : str
            Select first interface zones for pairing.
        zone2 : str
            Select second interface zones for pairing.
        zone1_list : typing.List[str]
            Select first interface defining this mesh-interface.
        zone2_list : typing.List[str]
            Select second interface defining this mesh-interface.
        mapped : bool
            Indicate if mesh-interface is mapped.
        enable_local_mapped_tolerance : bool
            Enable local tolerance for this mesh interface.
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        local_relative_mapped_tolerance : real
            Tolerance.
        local_absolute_mapped_tolerance : real
            Tolerance.
        periodic : bool
            Indicate if mesh-interface is adjacent to periodic boundaries.
        turbo : bool
            Create a general turbo interface.
        turbo_choice : str
            Enter your choice of pitch-change types.
        mixing_plane : bool
            If you want to use mixing plane mechanism.
        turbo_non_overlap : bool
            Create non-overlapping walls for gti interfaces.
        coupled : bool
            Indicate if mesh-interface is coupled.
        matching : bool
            Indicate if mesh-interface is matching.
        static : bool
            Indicate if mesh-interface is static.
    
    """

    fluent_name = "create"

    argument_names = \
        ['name', 'zone1', 'zone2', 'zone1_list', 'zone2_list', 'mapped',
         'enable_local_mapped_tolerance', 'use_local_edge_length_factor',
         'local_relative_mapped_tolerance', 'local_absolute_mapped_tolerance',
         'periodic', 'turbo', 'turbo_choice', 'mixing_plane',
         'turbo_non_overlap', 'coupled', 'matching', 'static']

    _child_classes = dict(
        name=name_cls,
        zone1=zone1_cls,
        zone2=zone2_cls,
        zone1_list=zone1_list_cls,
        zone2_list=zone2_list_cls,
        mapped=mapped_cls,
        enable_local_mapped_tolerance=enable_local_mapped_tolerance_cls,
        use_local_edge_length_factor=use_local_edge_length_factor_cls,
        local_relative_mapped_tolerance=local_relative_mapped_tolerance_cls,
        local_absolute_mapped_tolerance=local_absolute_mapped_tolerance_cls,
        periodic=periodic_cls,
        turbo=turbo_cls,
        turbo_choice=turbo_choice_cls,
        mixing_plane=mixing_plane_cls,
        turbo_non_overlap=turbo_non_overlap_cls,
        coupled=coupled_cls,
        matching=matching_cls,
        static=static_cls,
    )

