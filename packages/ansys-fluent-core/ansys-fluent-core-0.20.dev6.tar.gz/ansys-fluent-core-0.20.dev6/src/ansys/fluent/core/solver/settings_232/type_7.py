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

from .option import option as option_cls
from .hexahedron import hexahedron as hexahedron_cls
from .sphere import sphere as sphere_cls
from .cylinder import cylinder as cylinder_cls
from .boundary import boundary as boundary_cls
from .limiters import limiters as limiters_cls
from .field_value import field_value as field_value_cls
from .residual import residual as residual_cls
from .volume_1 import volume as volume_cls
from .yplus_star import yplus_star as yplus_star_cls
from .yplus_ystar import yplus_ystar as yplus_ystar_cls
class type(Group):
    """
    'type' child.
    """

    fluent_name = "type"

    child_names = \
        ['option', 'hexahedron', 'sphere', 'cylinder', 'boundary', 'limiters',
         'field_value', 'residual', 'volume', 'yplus_star', 'yplus_ystar']

    _child_classes = dict(
        option=option_cls,
        hexahedron=hexahedron_cls,
        sphere=sphere_cls,
        cylinder=cylinder_cls,
        boundary=boundary_cls,
        limiters=limiters_cls,
        field_value=field_value_cls,
        residual=residual_cls,
        volume=volume_cls,
        yplus_star=yplus_star_cls,
        yplus_ystar=yplus_ystar_cls,
    )

