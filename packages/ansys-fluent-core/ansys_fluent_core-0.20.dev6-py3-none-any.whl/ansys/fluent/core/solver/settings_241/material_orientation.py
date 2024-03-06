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

from .cursys_1 import cursys as cursys_cls
from .cursys_name import cursys_name as cursys_name_cls
class material_orientation(Group):
    """
    Help not available.
    """

    fluent_name = "material-orientation"

    child_names = \
        ['cursys', 'cursys_name']

    _child_classes = dict(
        cursys=cursys_cls,
        cursys_name=cursys_name_cls,
    )

