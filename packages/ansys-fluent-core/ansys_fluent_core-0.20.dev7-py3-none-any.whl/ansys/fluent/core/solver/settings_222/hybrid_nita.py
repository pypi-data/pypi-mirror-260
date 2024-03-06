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

from .outer_iterations import outer_iterations as outer_iterations_cls
from .initial_outer_iterations import initial_outer_iterations as initial_outer_iterations_cls
from .instability_detector import instability_detector as instability_detector_cls
class hybrid_nita(Group):
    """
    'hybrid_nita' child.
    """

    fluent_name = "hybrid-nita"

    child_names = \
        ['outer_iterations', 'initial_outer_iterations',
         'instability_detector']

    _child_classes = dict(
        outer_iterations=outer_iterations_cls,
        initial_outer_iterations=initial_outer_iterations_cls,
        instability_detector=instability_detector_cls,
    )

