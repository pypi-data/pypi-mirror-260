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
from .c1 import c1 as c1_cls
from .c2 import c2 as c2_cls
from .reference_viscosity import reference_viscosity as reference_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .effective_temperature import effective_temperature as effective_temperature_cls
class sutherland(Group):
    """
    'sutherland' child.
    """

    fluent_name = "sutherland"

    child_names = \
        ['option', 'c1', 'c2', 'reference_viscosity', 'reference_temperature',
         'effective_temperature']

    _child_classes = dict(
        option=option_cls,
        c1=c1_cls,
        c2=c2_cls,
        reference_viscosity=reference_viscosity_cls,
        reference_temperature=reference_temperature_cls,
        effective_temperature=effective_temperature_cls,
    )

