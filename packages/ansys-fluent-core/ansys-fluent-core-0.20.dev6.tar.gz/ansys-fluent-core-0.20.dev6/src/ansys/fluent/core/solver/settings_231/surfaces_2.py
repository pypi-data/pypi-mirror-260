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

from .plane_surface import plane_surface as plane_surface_cls
class surfaces(Group):
    """
    'surfaces' child.
    """

    fluent_name = "surfaces"

    child_names = \
        ['plane_surface']

    _child_classes = dict(
        plane_surface=plane_surface_cls,
    )

