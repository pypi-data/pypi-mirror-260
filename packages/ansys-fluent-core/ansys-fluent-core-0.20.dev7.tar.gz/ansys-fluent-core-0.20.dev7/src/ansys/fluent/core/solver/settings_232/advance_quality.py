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

from .bitrate_scale import bitrate_scale as bitrate_scale_cls
from .enable_h264 import enable_h264 as enable_h264_cls
from .bitrate import bitrate as bitrate_cls
from .compression_method import compression_method as compression_method_cls
from .keyframe import keyframe as keyframe_cls
class advance_quality(Group):
    """
    Advance Quality setting.
    """

    fluent_name = "advance-quality"

    child_names = \
        ['bitrate_scale', 'enable_h264', 'bitrate', 'compression_method',
         'keyframe']

    _child_classes = dict(
        bitrate_scale=bitrate_scale_cls,
        enable_h264=enable_h264_cls,
        bitrate=bitrate_cls,
        compression_method=compression_method_cls,
        keyframe=keyframe_cls,
    )

