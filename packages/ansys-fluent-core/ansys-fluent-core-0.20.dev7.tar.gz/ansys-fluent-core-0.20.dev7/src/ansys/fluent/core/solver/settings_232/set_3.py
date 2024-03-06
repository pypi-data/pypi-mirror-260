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

from .cell_function_2 import cell_function as cell_function_cls
from .load_distribution import load_distribution as load_distribution_cls
from .merge import merge as merge_cls
from .partition_origin_vector import partition_origin_vector as partition_origin_vector_cls
from .pre_test_1 import pre_test as pre_test_cls
from .smooth_1 import smooth as smooth_cls
from .print_verbosity import print_verbosity as print_verbosity_cls
from .origin_1 import origin as origin_cls
from .laplace_smoothing import laplace_smoothing as laplace_smoothing_cls
from .nfaces_as_weights_1 import nfaces_as_weights as nfaces_as_weights_cls
from .face_area_as_weights import face_area_as_weights as face_area_as_weights_cls
from .layering import layering as layering_cls
from .solid_thread_weight import solid_thread_weight as solid_thread_weight_cls
from .stretched_mesh_enhancement import stretched_mesh_enhancement as stretched_mesh_enhancement_cls
from .particle_weight import particle_weight as particle_weight_cls
from .vof_free_surface_weight import vof_free_surface_weight as vof_free_surface_weight_cls
from .isat_weight import isat_weight as isat_weight_cls
from .fluid_solid_rebalance_after_read_case import fluid_solid_rebalance_after_read_case as fluid_solid_rebalance_after_read_case_cls
from .model_weighted_partition import model_weighted_partition as model_weighted_partition_cls
from .dpm_load_balancing import dpm_load_balancing as dpm_load_balancing_cls
from .across_zones_1 import across_zones as across_zones_cls
from .all_off import all_off as all_off_cls
from .all_on import all_on as all_on_cls
class set(Group):
    """
    Enter the menu to set partition parameters.
    """

    fluent_name = "set"

    child_names = \
        ['cell_function', 'load_distribution', 'merge',
         'partition_origin_vector', 'pre_test', 'smooth', 'print_verbosity',
         'origin', 'laplace_smoothing', 'nfaces_as_weights',
         'face_area_as_weights', 'layering', 'solid_thread_weight',
         'stretched_mesh_enhancement', 'particle_weight',
         'vof_free_surface_weight', 'isat_weight',
         'fluid_solid_rebalance_after_read_case', 'model_weighted_partition',
         'dpm_load_balancing']

    command_names = \
        ['across_zones', 'all_off', 'all_on']

    _child_classes = dict(
        cell_function=cell_function_cls,
        load_distribution=load_distribution_cls,
        merge=merge_cls,
        partition_origin_vector=partition_origin_vector_cls,
        pre_test=pre_test_cls,
        smooth=smooth_cls,
        print_verbosity=print_verbosity_cls,
        origin=origin_cls,
        laplace_smoothing=laplace_smoothing_cls,
        nfaces_as_weights=nfaces_as_weights_cls,
        face_area_as_weights=face_area_as_weights_cls,
        layering=layering_cls,
        solid_thread_weight=solid_thread_weight_cls,
        stretched_mesh_enhancement=stretched_mesh_enhancement_cls,
        particle_weight=particle_weight_cls,
        vof_free_surface_weight=vof_free_surface_weight_cls,
        isat_weight=isat_weight_cls,
        fluid_solid_rebalance_after_read_case=fluid_solid_rebalance_after_read_case_cls,
        model_weighted_partition=model_weighted_partition_cls,
        dpm_load_balancing=dpm_load_balancing_cls,
        across_zones=across_zones_cls,
        all_off=all_off_cls,
        all_on=all_on_cls,
    )

