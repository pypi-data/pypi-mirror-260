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

from .re_randomize_every_iteration import re_randomize_every_iteration as re_randomize_every_iteration_cls
from .re_randomize_every_timestep import re_randomize_every_timestep as re_randomize_every_timestep_cls
from .tracking_statistics_format import tracking_statistics_format as tracking_statistics_format_cls
from .verbosity_1 import verbosity as verbosity_cls
class expert_options(Group):
    """
    Menu containing not frequently used (expert level) settings.
    """

    fluent_name = "expert-options"

    child_names = \
        ['re_randomize_every_iteration', 're_randomize_every_timestep',
         'tracking_statistics_format', 'verbosity']

    _child_classes = dict(
        re_randomize_every_iteration=re_randomize_every_iteration_cls,
        re_randomize_every_timestep=re_randomize_every_timestep_cls,
        tracking_statistics_format=tracking_statistics_format_cls,
        verbosity=verbosity_cls,
    )

