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

class quality(String, _HasAllowedValuesMixin):
    """
    Set the quality for raytracing. Higher quality leads to more refining of the raytraced image, which results in more time and memory consumption.
    """

    fluent_name = "quality"

