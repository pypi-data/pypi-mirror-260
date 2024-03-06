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

from .boundary_volume import boundary_volume as boundary_volume_cls
from .volume_growth import volume_growth as volume_growth_cls
class volume_distance(Group):
    """
    'volume_distance' child.
    """

    fluent_name = "volume-distance"

    child_names = \
        ['boundary_volume', 'volume_growth']

    _child_classes = dict(
        boundary_volume=boundary_volume_cls,
        volume_growth=volume_growth_cls,
    )

