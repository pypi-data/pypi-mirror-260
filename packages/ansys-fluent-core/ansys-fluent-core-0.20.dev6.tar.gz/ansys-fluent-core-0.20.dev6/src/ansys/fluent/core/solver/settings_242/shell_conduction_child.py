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

from .thickness import thickness as thickness_cls
from .material_2 import material as material_cls
from .qdot import qdot as qdot_cls
class shell_conduction_child(Group):
    """
    'child_object_type' of shell_conduction.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['thickness', 'material', 'qdot']

    _child_classes = dict(
        thickness=thickness_cls,
        material=material_cls,
        qdot=qdot_cls,
    )

