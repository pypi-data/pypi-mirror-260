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

from .solar_frequency_data import solar_frequency_data as solar_frequency_data_cls
from .solar_filename import solar_filename as solar_filename_cls
class autoread_solar_data(Group):
    """
    Set autoread solar data parameters.
    """

    fluent_name = "autoread-solar-data"

    child_names = \
        ['solar_frequency_data', 'solar_filename']

    _child_classes = dict(
        solar_frequency_data=solar_frequency_data_cls,
        solar_filename=solar_filename_cls,
    )

