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

from .enabled_14 import enabled as enabled_cls
from .source_file import source_file as source_file_cls
from .create_customized_addon_lib import create_customized_addon_lib as create_customized_addon_lib_cls
class customized_udf(Group):
    """
    'customized_udf' child.
    """

    fluent_name = "customized-udf"

    child_names = \
        ['enabled', 'source_file']

    command_names = \
        ['create_customized_addon_lib']

    _child_classes = dict(
        enabled=enabled_cls,
        source_file=source_file_cls,
        create_customized_addon_lib=create_customized_addon_lib_cls,
    )

