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

from .thickness_1 import thickness as thickness_cls
from .material import material as material_cls
from .qdot import qdot as qdot_cls
class thin_wall_child(Group):
    """
    'child_object_type' of thin_wall.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['thickness', 'material', 'qdot']

    _child_classes = dict(
        thickness=thickness_cls,
        material=material_cls,
        qdot=qdot_cls,
    )

