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

from .enable_20 import enable as enable_cls
from .disable_1 import disable as disable_cls
from .copy_3 import copy as copy_cls
from .delete_4 import delete as delete_cls
from .export_1 import export as export_cls
from .import__1 import import_ as import__cls
class execute_commands(Group):
    """
    'execute_commands' child.
    """

    fluent_name = "execute-commands"

    command_names = \
        ['enable', 'disable', 'copy', 'delete', 'export', 'import_']

    _child_classes = dict(
        enable=enable_cls,
        disable=disable_cls,
        copy=copy_cls,
        delete=delete_cls,
        export=export_cls,
        import_=import__cls,
    )

