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

from .modified_setting import modified_setting as modified_setting_cls
from .write_user_setting import write_user_setting as write_user_setting_cls
class modified_setting_options(Group):
    """
    'modified_setting_options' child.
    """

    fluent_name = "modified-setting-options"

    command_names = \
        ['modified_setting', 'write_user_setting']

    _child_classes = dict(
        modified_setting=modified_setting_cls,
        write_user_setting=write_user_setting_cls,
    )

