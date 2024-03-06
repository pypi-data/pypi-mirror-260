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

from .formulation import formulation as formulation_cls
from .relaxation_method_1 import relaxation_method as relaxation_method_cls
from .convergence_acceleration_for_stretched_meshes_1 import convergence_acceleration_for_stretched_meshes as convergence_acceleration_for_stretched_meshes_cls
from .relaxation_bounds import relaxation_bounds as relaxation_bounds_cls
class pseudo_time_method(Group):
    """
    Enter the pseudo time method menu.
    """

    fluent_name = "pseudo-time-method"

    child_names = \
        ['formulation', 'relaxation_method',
         'convergence_acceleration_for_stretched_meshes']

    command_names = \
        ['relaxation_bounds']

    _child_classes = dict(
        formulation=formulation_cls,
        relaxation_method=relaxation_method_cls,
        convergence_acceleration_for_stretched_meshes=convergence_acceleration_for_stretched_meshes_cls,
        relaxation_bounds=relaxation_bounds_cls,
    )

