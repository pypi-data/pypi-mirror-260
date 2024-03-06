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

from .ambient_color import ambient_color as ambient_color_cls
from .headlight_setting import headlight_setting as headlight_setting_cls
from .lights_on import lights_on as lights_on_cls
from .lighting_interpolation import lighting_interpolation as lighting_interpolation_cls
from .set_light import set_light as set_light_cls
class lights(Group):
    """
    'lights' child.
    """

    fluent_name = "lights"

    child_names = \
        ['ambient_color', 'headlight_setting', 'lights_on',
         'lighting_interpolation']

    command_names = \
        ['set_light']

    _child_classes = dict(
        ambient_color=ambient_color_cls,
        headlight_setting=headlight_setting_cls,
        lights_on=lights_on_cls,
        lighting_interpolation=lighting_interpolation_cls,
        set_light=set_light_cls,
    )

