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

from .calculation_method import calculation_method as calculation_method_cls
class htc(Group):
    """
    Enter the heat transfer coeficient menu.
    """

    fluent_name = "htc"

    child_names = \
        ['calculation_method']

    _child_classes = dict(
        calculation_method=calculation_method_cls,
    )

