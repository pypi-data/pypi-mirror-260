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

class lighting_interpolation(String, _HasAllowedValuesMixin):
    """
    Set lighting interpolation method.
    Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.
    Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.
    Use flat shading for meshes and polygons.
    """

    fluent_name = "lighting-interpolation"

