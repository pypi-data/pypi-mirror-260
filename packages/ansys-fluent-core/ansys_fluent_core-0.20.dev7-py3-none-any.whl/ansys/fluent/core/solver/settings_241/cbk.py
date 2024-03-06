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
from .char_intrinsic_reactivity import char_intrinsic_reactivity as char_intrinsic_reactivity_cls
from .carbon_content_percentage import carbon_content_percentage as carbon_content_percentage_cls
class cbk(Group):
    """
    'cbk' child.
    """

    fluent_name = "cbk"

    child_names = \
        ['option', 'char_intrinsic_reactivity', 'carbon_content_percentage']

    _child_classes = dict(
        option=option_cls,
        char_intrinsic_reactivity=char_intrinsic_reactivity_cls,
        carbon_content_percentage=carbon_content_percentage_cls,
    )

