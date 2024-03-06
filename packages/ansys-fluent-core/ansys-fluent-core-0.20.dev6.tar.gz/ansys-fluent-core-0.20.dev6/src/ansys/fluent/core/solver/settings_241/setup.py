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

from .general import general as general_cls
from .models_1 import models as models_cls
from .materials import materials as materials_cls
from .cell_zone_conditions import cell_zone_conditions as cell_zone_conditions_cls
from .boundary_conditions import boundary_conditions as boundary_conditions_cls
from .mesh_interfaces import mesh_interfaces as mesh_interfaces_cls
from .reference_values import reference_values as reference_values_cls
from .reference_frames import reference_frames as reference_frames_cls
from .named_expressions import named_expressions as named_expressions_cls
from .turbo_models import turbo_models as turbo_models_cls
from .geometry_4 import geometry as geometry_cls
from .physics import physics as physics_cls
class setup(Group):
    """
    'setup' child.
    """

    fluent_name = "setup"

    child_names = \
        ['general', 'models', 'materials', 'cell_zone_conditions',
         'boundary_conditions', 'mesh_interfaces', 'reference_values',
         'reference_frames', 'named_expressions', 'turbo_models', 'geometry',
         'physics']

    _child_classes = dict(
        general=general_cls,
        models=models_cls,
        materials=materials_cls,
        cell_zone_conditions=cell_zone_conditions_cls,
        boundary_conditions=boundary_conditions_cls,
        mesh_interfaces=mesh_interfaces_cls,
        reference_values=reference_values_cls,
        reference_frames=reference_frames_cls,
        named_expressions=named_expressions_cls,
        turbo_models=turbo_models_cls,
        geometry=geometry_cls,
        physics=physics_cls,
    )

