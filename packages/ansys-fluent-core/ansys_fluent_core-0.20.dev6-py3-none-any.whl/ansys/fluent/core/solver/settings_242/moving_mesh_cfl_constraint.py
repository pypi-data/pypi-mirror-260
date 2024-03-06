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

from .moving_mesh_constraint import moving_mesh_constraint as moving_mesh_constraint_cls
from .mesh_courant_number import mesh_courant_number as mesh_courant_number_cls
class moving_mesh_cfl_constraint(Group):
    """
    Enter moving mesh CFL constraint menu.
    """

    fluent_name = "moving-mesh-cfl-constraint"

    child_names = \
        ['moving_mesh_constraint', 'mesh_courant_number']

    _child_classes = dict(
        moving_mesh_constraint=moving_mesh_constraint_cls,
        mesh_courant_number=mesh_courant_number_cls,
    )

