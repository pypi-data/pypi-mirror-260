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

from .general_settings import general_settings as general_settings_cls
from .turbulent_setting import turbulent_setting as turbulent_setting_cls
class set_hybrid_init_options(Group):
    """
    'set_hybrid_init_options' child.
    """

    fluent_name = "set-hybrid-init-options"

    child_names = \
        ['general_settings', 'turbulent_setting']

    _child_classes = dict(
        general_settings=general_settings_cls,
        turbulent_setting=turbulent_setting_cls,
    )

