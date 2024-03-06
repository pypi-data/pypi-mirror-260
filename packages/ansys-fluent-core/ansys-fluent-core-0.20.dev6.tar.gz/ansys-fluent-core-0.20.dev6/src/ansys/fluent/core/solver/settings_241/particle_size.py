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

from .diameter import diameter as diameter_cls
from .diameter_2 import diameter_2 as diameter_2_cls
from .option import option as option_cls
from .rosin_rammler import rosin_rammler as rosin_rammler_cls
from .tabulated_size import tabulated_size as tabulated_size_cls
class particle_size(Group):
    """
    'particle_size' child.
    """

    fluent_name = "particle-size"

    child_names = \
        ['diameter', 'diameter_2', 'option', 'rosin_rammler',
         'tabulated_size']

    _child_classes = dict(
        diameter=diameter_cls,
        diameter_2=diameter_2_cls,
        option=option_cls,
        rosin_rammler=rosin_rammler_cls,
        tabulated_size=tabulated_size_cls,
    )

