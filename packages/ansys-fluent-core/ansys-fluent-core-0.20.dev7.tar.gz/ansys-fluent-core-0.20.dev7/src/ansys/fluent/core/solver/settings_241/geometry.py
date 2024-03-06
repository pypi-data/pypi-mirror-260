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

from .reconstruct_geometry import reconstruct_geometry as reconstruct_geometry_cls
class geometry(Group):
    """
    Enter the adaption geometry menu.
    """

    fluent_name = "geometry"

    child_names = \
        ['reconstruct_geometry']

    _child_classes = dict(
        reconstruct_geometry=reconstruct_geometry_cls,
    )

