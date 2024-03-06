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

from .isat_error_tolerance import isat_error_tolerance as isat_error_tolerance_cls
from .isat_table_size import isat_table_size as isat_table_size_cls
from .isat_verbosity import isat_verbosity as isat_verbosity_cls
from .clear_isat_table import clear_isat_table as clear_isat_table_cls
class isat_options(Group):
    """
    'isat_options' child.
    """

    fluent_name = "isat-options"

    child_names = \
        ['isat_error_tolerance', 'isat_table_size', 'isat_verbosity']

    command_names = \
        ['clear_isat_table']

    _child_classes = dict(
        isat_error_tolerance=isat_error_tolerance_cls,
        isat_table_size=isat_table_size_cls,
        isat_verbosity=isat_verbosity_cls,
        clear_isat_table=clear_isat_table_cls,
    )

