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

from .a_2 import a as a_cls
from .b import b as b_cls
from .c import c as c_cls
class blottner_curve_fit(Group):
    """
    'blottner_curve_fit' child.
    """

    fluent_name = "blottner-curve-fit"

    child_names = \
        ['a', 'b', 'c']

    _child_classes = dict(
        a=a_cls,
        b=b_cls,
        c=c_cls,
    )

