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
from .option_12 import option as option_cls
from .scaling import scaling as scaling_cls
from .derivative import derivative as derivative_cls
from .size_ratio import size_ratio as size_ratio_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls
class field_value(Group):
    """
    'field_value' child.
    """

    fluent_name = "field-value"

    child_names = \
        ['field', 'option', 'scaling', 'derivative', 'size_ratio',
         'create_volume_surface']

    _child_classes = dict(
        field=field_cls,
        option=option_cls,
        scaling=scaling_cls,
        derivative=derivative_cls,
        size_ratio=size_ratio_cls,
        create_volume_surface=create_volume_surface_cls,
    )

