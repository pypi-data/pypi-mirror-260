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

from .feature_angle import feature_angle as feature_angle_cls
class feature(Group):
    """
    'feature' child.
    """

    fluent_name = "feature"

    child_names = \
        ['feature_angle']

    _child_classes = dict(
        feature_angle=feature_angle_cls,
    )

