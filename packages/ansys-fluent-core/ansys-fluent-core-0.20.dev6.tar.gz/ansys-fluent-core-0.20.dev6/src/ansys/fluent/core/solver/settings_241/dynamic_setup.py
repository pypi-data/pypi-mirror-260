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

from .method_6 import method as method_cls
from .dynamic_injection import dynamic_injection as dynamic_injection_cls
class dynamic_setup(Group):
    """
    'dynamic_setup' child.
    """

    fluent_name = "dynamic-setup"

    child_names = \
        ['method', 'dynamic_injection']

    _child_classes = dict(
        method=method_cls,
        dynamic_injection=dynamic_injection_cls,
    )

