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

from .hardcopy_format import hardcopy_format as hardcopy_format_cls
from .hardcopy_options import hardcopy_options as hardcopy_options_cls
from .window_dump_cmd import window_dump_cmd as window_dump_cmd_cls
from .post_format import post_format as post_format_cls
from .current_driver import current_driver as current_driver_cls
class driver_options(Group):
    """
    'driver_options' child.
    """

    fluent_name = "driver-options"

    child_names = \
        ['hardcopy_format', 'hardcopy_options', 'window_dump_cmd',
         'post_format']

    command_names = \
        ['current_driver']

    _child_classes = dict(
        hardcopy_format=hardcopy_format_cls,
        hardcopy_options=hardcopy_options_cls,
        window_dump_cmd=window_dump_cmd_cls,
        post_format=post_format_cls,
        current_driver=current_driver_cls,
    )

