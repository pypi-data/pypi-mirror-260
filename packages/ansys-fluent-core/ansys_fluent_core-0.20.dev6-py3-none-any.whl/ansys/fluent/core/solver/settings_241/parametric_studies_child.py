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

from .name import name as name_cls
from .design_points_1 import design_points as design_points_cls
from .current_design_point import current_design_point as current_design_point_cls
class parametric_studies_child(Group):
    """
    'child_object_type' of parametric_studies.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'design_points', 'current_design_point']

    _child_classes = dict(
        name=name_cls,
        design_points=design_points_cls,
        current_design_point=current_design_point_cls,
    )

