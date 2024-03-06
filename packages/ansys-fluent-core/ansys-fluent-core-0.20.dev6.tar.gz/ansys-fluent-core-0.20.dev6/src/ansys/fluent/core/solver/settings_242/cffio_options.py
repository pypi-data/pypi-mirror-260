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

from .io_mode import io_mode as io_mode_cls
from .compression_level import compression_level as compression_level_cls
from .single_precision_data import single_precision_data as single_precision_data_cls
class cffio_options(Group):
    """
    CFF I/O options.
    """

    fluent_name = "cffio-options"

    child_names = \
        ['io_mode', 'compression_level', 'single_precision_data']

    _child_classes = dict(
        io_mode=io_mode_cls,
        compression_level=compression_level_cls,
        single_precision_data=single_precision_data_cls,
    )

