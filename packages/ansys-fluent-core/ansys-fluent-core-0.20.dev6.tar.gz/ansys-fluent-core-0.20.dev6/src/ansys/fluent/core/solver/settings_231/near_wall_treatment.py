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

from .wall_function_1 import wall_function as wall_function_cls
from .law_of_the_wall import law_of_the_wall as law_of_the_wall_cls
from .enhanced_wall_treatment_options import enhanced_wall_treatment_options as enhanced_wall_treatment_options_cls
from .wall_omega_treatment import wall_omega_treatment as wall_omega_treatment_cls
class near_wall_treatment(Group):
    """
    'near_wall_treatment' child.
    """

    fluent_name = "near-wall-treatment"

    child_names = \
        ['wall_function', 'law_of_the_wall',
         'enhanced_wall_treatment_options', 'wall_omega_treatment']

    _child_classes = dict(
        wall_function=wall_function_cls,
        law_of_the_wall=law_of_the_wall_cls,
        enhanced_wall_treatment_options=enhanced_wall_treatment_options_cls,
        wall_omega_treatment=wall_omega_treatment_cls,
    )

