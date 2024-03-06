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

from .display_3 import display as display_cls
from .history_filename import history_filename as history_filename_cls
from .report_default_variables import report_default_variables as report_default_variables_cls
from .track_single_particle_stream_1 import track_single_particle_stream as track_single_particle_stream_cls
from .arrow_scale_1 import arrow_scale as arrow_scale_cls
from .arrow_space_1 import arrow_space as arrow_space_cls
from .coarsen_factor import coarsen_factor as coarsen_factor_cls
from .line_width_1 import line_width as line_width_cls
class particle_tracks(Group):
    """
    'particle_tracks' child.
    """

    fluent_name = "particle-tracks"

    child_names = \
        ['display', 'history_filename', 'report_default_variables',
         'track_single_particle_stream', 'arrow_scale', 'arrow_space',
         'coarsen_factor', 'line_width']

    _child_classes = dict(
        display=display_cls,
        history_filename=history_filename_cls,
        report_default_variables=report_default_variables_cls,
        track_single_particle_stream=track_single_particle_stream_cls,
        arrow_scale=arrow_scale_cls,
        arrow_space=arrow_space_cls,
        coarsen_factor=coarsen_factor_cls,
        line_width=line_width_cls,
    )

