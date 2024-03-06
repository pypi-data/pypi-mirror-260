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

from .relaxation_bounding_method import relaxation_bounding_method as relaxation_bounding_method_cls
from .default_min_max_relaxation_limits import default_min_max_relaxation_limits as default_min_max_relaxation_limits_cls
from .minimum_allowed_effctive_relaxation import minimum_allowed_effctive_relaxation as minimum_allowed_effctive_relaxation_cls
from .maximum_allowed_effctive_relaxation import maximum_allowed_effctive_relaxation as maximum_allowed_effctive_relaxation_cls
class relaxation_bounds(Command):
    """
    Select relaxation bounding scheme for pseudo time method.
    
    Parameters
    ----------
        relaxation_bounding_method : str
            'relaxation_bounding_method' child.
        default_min_max_relaxation_limits : bool
            'default_min_max_relaxation_limits' child.
        minimum_allowed_effctive_relaxation : real
            'minimum_allowed_effctive_relaxation' child.
        maximum_allowed_effctive_relaxation : real
            'maximum_allowed_effctive_relaxation' child.
    
    """

    fluent_name = "relaxation-bounds"

    argument_names = \
        ['relaxation_bounding_method', 'default_min_max_relaxation_limits',
         'minimum_allowed_effctive_relaxation',
         'maximum_allowed_effctive_relaxation']

    _child_classes = dict(
        relaxation_bounding_method=relaxation_bounding_method_cls,
        default_min_max_relaxation_limits=default_min_max_relaxation_limits_cls,
        minimum_allowed_effctive_relaxation=minimum_allowed_effctive_relaxation_cls,
        maximum_allowed_effctive_relaxation=maximum_allowed_effctive_relaxation_cls,
    )

