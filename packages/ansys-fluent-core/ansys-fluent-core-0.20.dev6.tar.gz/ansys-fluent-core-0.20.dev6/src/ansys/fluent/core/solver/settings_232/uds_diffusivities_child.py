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

from .option_10 import option as option_cls
from .value_1 import value as value_cls
from .expression import expression as expression_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .anisotropic import anisotropic as anisotropic_cls
from .orthotropic import orthotropic as orthotropic_cls
from .cyl_orthotropic import cyl_orthotropic as cyl_orthotropic_cls
class uds_diffusivities_child(Group):
    """
    'child_object_type' of uds_diffusivities.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'expression', 'polynomial',
         'user_defined_function', 'anisotropic', 'orthotropic',
         'cyl_orthotropic']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        expression=expression_cls,
        polynomial=polynomial_cls,
        user_defined_function=user_defined_function_cls,
        anisotropic=anisotropic_cls,
        orthotropic=orthotropic_cls,
        cyl_orthotropic=cyl_orthotropic_cls,
    )

