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

from .field import field as field_cls
from .scalefactor import scalefactor as scalefactor_cls
class ribbon_settings(Group):
    """
    'ribbon_settings' child.
    """

    fluent_name = "ribbon-settings"

    child_names = \
        ['field', 'scalefactor']

    _child_classes = dict(
        field=field_cls,
        scalefactor=scalefactor_cls,
    )

