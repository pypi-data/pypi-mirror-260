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
from .reference_values import reference_values as reference_values_cls
from .named_expressions import named_expressions as named_expressions_cls
class setup(Group):
    """
    'setup' child.
    """

    fluent_name = "setup"

    child_names = \
        ['general', 'models', 'materials', 'cell_zone_conditions',
         'boundary_conditions', 'reference_values', 'named_expressions']

    _child_classes = dict(
        general=general_cls,
        models=models_cls,
        materials=materials_cls,
        cell_zone_conditions=cell_zone_conditions_cls,
        boundary_conditions=boundary_conditions_cls,
        reference_values=reference_values_cls,
        named_expressions=named_expressions_cls,
    )

