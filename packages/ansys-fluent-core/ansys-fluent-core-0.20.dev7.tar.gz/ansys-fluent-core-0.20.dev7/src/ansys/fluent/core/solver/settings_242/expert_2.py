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

from .randomize_every_iteration import randomize_every_iteration as randomize_every_iteration_cls
from .randomize_every_timestep import randomize_every_timestep as randomize_every_timestep_cls
from .tracking_statistics_format import tracking_statistics_format as tracking_statistics_format_cls
from .verbosity_1 import verbosity as verbosity_cls
class expert(Group):
    """
    Menu containing not frequently used (expert level) settings.
    """

    fluent_name = "expert"

    child_names = \
        ['randomize_every_iteration', 'randomize_every_timestep',
         'tracking_statistics_format', 'verbosity']

    _child_classes = dict(
        randomize_every_iteration=randomize_every_iteration_cls,
        randomize_every_timestep=randomize_every_timestep_cls,
        tracking_statistics_format=tracking_statistics_format_cls,
        verbosity=verbosity_cls,
    )

