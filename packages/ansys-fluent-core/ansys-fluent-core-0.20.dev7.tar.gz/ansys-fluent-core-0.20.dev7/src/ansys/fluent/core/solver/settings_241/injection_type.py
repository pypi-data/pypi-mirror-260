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

from .option import option as option_cls
from .cone_type import cone_type as cone_type_cls
from .inject_as_film import inject_as_film as inject_as_film_cls
from .filename_2 import filename as filename_cls
class injection_type(Group):
    """
    'injection_type' child.
    """

    fluent_name = "injection-type"

    child_names = \
        ['option', 'cone_type', 'inject_as_film', 'filename']

    _child_classes = dict(
        option=option_cls,
        cone_type=cone_type_cls,
        inject_as_film=inject_as_film_cls,
        filename=filename_cls,
    )

