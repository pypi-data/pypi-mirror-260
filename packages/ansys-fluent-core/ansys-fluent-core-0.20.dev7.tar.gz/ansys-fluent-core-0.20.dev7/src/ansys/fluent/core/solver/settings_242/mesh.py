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

from .adapt import adapt as adapt_cls
from .anisotropic_adaption import anisotropic_adaption as anisotropic_adaption_cls
from .check_before_solve import check_before_solve as check_before_solve_cls
from .check_verbosity import check_verbosity as check_verbosity_cls
from .enhanced_orthogonal_quality import enhanced_orthogonal_quality as enhanced_orthogonal_quality_cls
from .matching_tolerance import matching_tolerance as matching_tolerance_cls
from .modify_zones import modify_zones as modify_zones_cls
from .show_periodic_shadow_zones import show_periodic_shadow_zones as show_periodic_shadow_zones_cls
from .reorder import reorder as reorder_cls
from .repair_improve import repair_improve as repair_improve_cls
from .surface_mesh import surface_mesh as surface_mesh_cls
from .polyhedra import polyhedra as polyhedra_cls
from .wall_distance_method import wall_distance_method as wall_distance_method_cls
from .adjacency import adjacency as adjacency_cls
from .check import check as check_cls
from .memory_usage import memory_usage as memory_usage_cls
from .mesh_info import mesh_info as mesh_info_cls
from .quality import quality as quality_cls
from .rotate import rotate as rotate_cls
from .scale_1 import scale as scale_cls
from .size_info import size_info as size_info_cls
from .redistribute_boundary_layer import redistribute_boundary_layer as redistribute_boundary_layer_cls
from .swap_mesh_faces import swap_mesh_faces as swap_mesh_faces_cls
from .smooth_mesh import smooth_mesh as smooth_mesh_cls
from .replace import replace as replace_cls
from .translate_1 import translate as translate_cls
class mesh(Group):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    child_names = \
        ['adapt', 'anisotropic_adaption', 'check_before_solve',
         'check_verbosity', 'enhanced_orthogonal_quality',
         'matching_tolerance', 'modify_zones', 'show_periodic_shadow_zones',
         'reorder', 'repair_improve', 'surface_mesh', 'polyhedra',
         'wall_distance_method']

    command_names = \
        ['adjacency', 'check', 'memory_usage', 'mesh_info', 'quality',
         'rotate', 'scale', 'size_info', 'redistribute_boundary_layer',
         'swap_mesh_faces', 'smooth_mesh', 'replace', 'translate']

    _child_classes = dict(
        adapt=adapt_cls,
        anisotropic_adaption=anisotropic_adaption_cls,
        check_before_solve=check_before_solve_cls,
        check_verbosity=check_verbosity_cls,
        enhanced_orthogonal_quality=enhanced_orthogonal_quality_cls,
        matching_tolerance=matching_tolerance_cls,
        modify_zones=modify_zones_cls,
        show_periodic_shadow_zones=show_periodic_shadow_zones_cls,
        reorder=reorder_cls,
        repair_improve=repair_improve_cls,
        surface_mesh=surface_mesh_cls,
        polyhedra=polyhedra_cls,
        wall_distance_method=wall_distance_method_cls,
        adjacency=adjacency_cls,
        check=check_cls,
        memory_usage=memory_usage_cls,
        mesh_info=mesh_info_cls,
        quality=quality_cls,
        rotate=rotate_cls,
        scale=scale_cls,
        size_info=size_info_cls,
        redistribute_boundary_layer=redistribute_boundary_layer_cls,
        swap_mesh_faces=swap_mesh_faces_cls,
        smooth_mesh=smooth_mesh_cls,
        replace=replace_cls,
        translate=translate_cls,
    )

