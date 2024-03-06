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

from .method_8 import method as method_cls
from .static_injection import static_injection as static_injection_cls
class static_setup(Group):
    """
    'static_setup' child.
    """

    fluent_name = "static-setup"

    child_names = \
        ['method', 'static_injection']

    _child_classes = dict(
        method=method_cls,
        static_injection=static_injection_cls,
    )

