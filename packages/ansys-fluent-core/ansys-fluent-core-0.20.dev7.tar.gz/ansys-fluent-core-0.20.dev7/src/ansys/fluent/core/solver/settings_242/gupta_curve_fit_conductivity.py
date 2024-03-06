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
from .d import d as d_cls
from .e_2 import e as e_cls
class gupta_curve_fit_conductivity(Group):
    """
    'gupta_curve_fit_conductivity' child.
    """

    fluent_name = "gupta-curve-fit-conductivity"

    child_names = \
        ['a', 'b', 'c', 'd', 'e']

    _child_classes = dict(
        a=a_cls,
        b=b_cls,
        c=c_cls,
        d=d_cls,
        e=e_cls,
    )

