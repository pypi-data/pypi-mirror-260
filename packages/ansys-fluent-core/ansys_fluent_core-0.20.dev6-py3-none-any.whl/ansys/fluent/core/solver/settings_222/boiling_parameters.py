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

from .thin_film import thin_film as thin_film_cls
from .liquid_vof_factor import liquid_vof_factor as liquid_vof_factor_cls
class boiling_parameters(Group):
    """
    'boiling_parameters' child.
    """

    fluent_name = "boiling-parameters"

    child_names = \
        ['thin_film', 'liquid_vof_factor']

    _child_classes = dict(
        thin_film=thin_film_cls,
        liquid_vof_factor=liquid_vof_factor_cls,
    )

