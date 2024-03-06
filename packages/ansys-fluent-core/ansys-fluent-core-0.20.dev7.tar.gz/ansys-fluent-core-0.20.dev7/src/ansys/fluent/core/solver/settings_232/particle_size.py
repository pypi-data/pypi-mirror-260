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
from .rosin_rammler_settings import rosin_rammler_settings as rosin_rammler_settings_cls
from .tabulated_size_settings import tabulated_size_settings as tabulated_size_settings_cls
class particle_size(Group):
    """
    'particle_size' child.
    """

    fluent_name = "particle-size"

    child_names = \
        ['diameter', 'diameter_2', 'option', 'rosin_rammler_settings',
         'tabulated_size_settings']

    _child_classes = dict(
        diameter=diameter_cls,
        diameter_2=diameter_2_cls,
        option=option_cls,
        rosin_rammler_settings=rosin_rammler_settings_cls,
        tabulated_size_settings=tabulated_size_settings_cls,
    )

