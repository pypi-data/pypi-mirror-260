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

from .enable_gpu import enable_gpu as enable_gpu_cls
from .term_criterion import term_criterion as term_criterion_cls
from .solver_1 import solver as solver_cls
from .max_num_cycle import max_num_cycle as max_num_cycle_cls
from .coarsen_by_size import coarsen_by_size as coarsen_by_size_cls
from .pre_sweep import pre_sweep as pre_sweep_cls
from .post_sweep import post_sweep as post_sweep_cls
from .smoother import smoother as smoother_cls
class amg_gpgpu_options_child(Group):
    """
    'child_object_type' of amg_gpgpu_options.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['enable_gpu', 'term_criterion', 'solver', 'max_num_cycle',
         'coarsen_by_size', 'pre_sweep', 'post_sweep', 'smoother']

    _child_classes = dict(
        enable_gpu=enable_gpu_cls,
        term_criterion=term_criterion_cls,
        solver=solver_cls,
        max_num_cycle=max_num_cycle_cls,
        coarsen_by_size=coarsen_by_size_cls,
        pre_sweep=pre_sweep_cls,
        post_sweep=post_sweep_cls,
        smoother=smoother_cls,
    )

