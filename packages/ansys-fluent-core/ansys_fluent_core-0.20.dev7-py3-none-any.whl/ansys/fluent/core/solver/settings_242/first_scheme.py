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

from .method_14 import method as method_cls
from .auto_detection import auto_detection as auto_detection_cls
from .iterations_2 import iterations as iterations_cls
from .dissipation import dissipation as dissipation_cls
class first_scheme(Group):
    """
    First adjoint stabilization scheme controls menu.
    """

    fluent_name = "first-scheme"

    child_names = \
        ['method', 'auto_detection', 'iterations', 'dissipation']

    _child_classes = dict(
        method=method_cls,
        auto_detection=auto_detection_cls,
        iterations=iterations_cls,
        dissipation=dissipation_cls,
    )

