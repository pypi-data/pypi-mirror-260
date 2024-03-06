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

from .change_numerics import change_numerics as change_numerics_cls
class non_conformal_interface_numerics(Group):
    """
    Setting non-conformal numerics options.
    """

    fluent_name = "non-conformal-interface-numerics"

    command_names = \
        ['change_numerics']

    _child_classes = dict(
        change_numerics=change_numerics_cls,
    )

