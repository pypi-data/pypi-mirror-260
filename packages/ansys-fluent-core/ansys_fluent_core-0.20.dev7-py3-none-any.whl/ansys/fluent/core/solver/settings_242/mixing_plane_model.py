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

from .bands_type import bands_type as bands_type_cls
from .number_of_bands import number_of_bands as number_of_bands_cls
from .list_mixing_planes import list_mixing_planes as list_mixing_planes_cls
class mixing_plane_model(Group):
    """
    Set the expert parameters for turbo interfaces.
    """

    fluent_name = "mixing-plane-model"

    child_names = \
        ['bands_type', 'number_of_bands']

    command_names = \
        ['list_mixing_planes']

    _child_classes = dict(
        bands_type=bands_type_cls,
        number_of_bands=number_of_bands_cls,
        list_mixing_planes=list_mixing_planes_cls,
    )

