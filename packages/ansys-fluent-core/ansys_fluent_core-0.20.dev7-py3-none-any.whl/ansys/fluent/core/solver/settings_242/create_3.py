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

from .coefficients_3 import coefficients as coefficients_cls
from .distance import distance as distance_cls
class create(Command):
    """
    To define a mirror plane for a non-symmetric domain.
    
    Parameters
    ----------
        coefficients : typing.List[real]
            Set the cofficients of X, Y and Z.
        distance : real
            Set the distance of the plane from the origin.
    
    """

    fluent_name = "create"

    argument_names = \
        ['coefficients', 'distance']

    _child_classes = dict(
        coefficients=coefficients_cls,
        distance=distance_cls,
    )

