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

from .named_expressions import named_expressions as named_expressions_cls
from .templated import templated as templated_cls
from .selection import selection as selection_cls
class observables(Group):
    """
    Enter the postprocessing options menu.
    """

    fluent_name = "observables"

    child_names = \
        ['named_expressions', 'templated', 'selection']

    _child_classes = dict(
        named_expressions=named_expressions_cls,
        templated=templated_cls,
        selection=selection_cls,
    )

