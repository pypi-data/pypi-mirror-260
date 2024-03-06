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

from .option_3 import option as option_cls
from .const_number_in_parcel import const_number_in_parcel as const_number_in_parcel_cls
from .const_parcel_mass import const_parcel_mass as const_parcel_mass_cls
from .const_parcel_diameter import const_parcel_diameter as const_parcel_diameter_cls
class parcel_method(Group):
    """
    'parcel_method' child.
    """

    fluent_name = "parcel-method"

    child_names = \
        ['option', 'const_number_in_parcel', 'const_parcel_mass',
         'const_parcel_diameter']

    _child_classes = dict(
        option=option_cls,
        const_number_in_parcel=const_number_in_parcel_cls,
        const_parcel_mass=const_parcel_mass_cls,
        const_parcel_diameter=const_parcel_diameter_cls,
    )

