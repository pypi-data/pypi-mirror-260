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

from .band_width import band_width as band_width_cls
from .reorder_domain import reorder_domain as reorder_domain_cls
from .reorder_zones import reorder_zones as reorder_zones_cls
class reorder(Group):
    """
    Enter the reorder domain menu.
    """

    fluent_name = "reorder"

    command_names = \
        ['band_width', 'reorder_domain', 'reorder_zones']

    _child_classes = dict(
        band_width=band_width_cls,
        reorder_domain=reorder_domain_cls,
        reorder_zones=reorder_zones_cls,
    )

