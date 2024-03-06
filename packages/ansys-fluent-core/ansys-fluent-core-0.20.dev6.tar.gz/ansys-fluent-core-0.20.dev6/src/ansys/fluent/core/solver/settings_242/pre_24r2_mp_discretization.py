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

from .enabled_32 import enabled as enabled_cls
class pre_24r2_mp_discretization(Command):
    """
    Pre 24R2 discretization for the mixing-plane.
    
    Parameters
    ----------
        enabled : bool
            Enable/Disable enhanced discretization for the mixing-plane.
    
    """

    fluent_name = "pre-24r2-mp-discretization"

    argument_names = \
        ['enabled']

    _child_classes = dict(
        enabled=enabled_cls,
    )

