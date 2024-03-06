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

from .physical_models_2 import physical_models as physical_models_cls
from .dynamic_mesh import dynamic_mesh as dynamic_mesh_cls
from .mesh_adaption import mesh_adaption as mesh_adaption_cls
class load_balance(Group):
    """
    'load_balance' child.
    """

    fluent_name = "load-balance"

    child_names = \
        ['physical_models', 'dynamic_mesh', 'mesh_adaption']

    _child_classes = dict(
        physical_models=physical_models_cls,
        dynamic_mesh=dynamic_mesh_cls,
        mesh_adaption=mesh_adaption_cls,
    )

