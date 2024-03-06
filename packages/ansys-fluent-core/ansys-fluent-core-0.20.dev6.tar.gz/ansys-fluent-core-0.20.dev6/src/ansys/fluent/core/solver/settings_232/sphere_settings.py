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

from .scale_2 import scale as scale_cls
from .sphere_lod import sphere_lod as sphere_lod_cls
from .options_12 import options as options_cls
class sphere_settings(Group):
    """
    'sphere_settings' child.
    """

    fluent_name = "sphere-settings"

    child_names = \
        ['scale', 'sphere_lod', 'options']

    _child_classes = dict(
        scale=scale_cls,
        sphere_lod=sphere_lod_cls,
        options=options_cls,
    )

