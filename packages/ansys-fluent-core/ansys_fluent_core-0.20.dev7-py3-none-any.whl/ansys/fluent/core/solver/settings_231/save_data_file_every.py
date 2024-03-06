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

from .frequency_type import frequency_type as frequency_type_cls
from .save_frequency import save_frequency as save_frequency_cls
class save_data_file_every(Group):
    """
    Set the auto save frequency type to either time-step or crank-angle and set the corresponding frequency.
    """

    fluent_name = "save-data-file-every"

    child_names = \
        ['frequency_type', 'save_frequency']

    _child_classes = dict(
        frequency_type=frequency_type_cls,
        save_frequency=save_frequency_cls,
    )

