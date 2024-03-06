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

from .mass_average import mass_average as mass_average_cls
from .mass_integral import mass_integral as mass_integral_cls
from .mass import mass as mass_cls
from .sum_1 import sum as sum_cls
from .twopisum import twopisum as twopisum_cls
from .minimum_2 import minimum as minimum_cls
from .maximum_2 import maximum as maximum_cls
from .volume_2 import volume as volume_cls
from .volume_average import volume_average as volume_average_cls
from .volume_integral import volume_integral as volume_integral_cls
class volume_integrals(Group):
    """
    'volume_integrals' child.
    """

    fluent_name = "volume-integrals"

    command_names = \
        ['mass_average', 'mass_integral', 'mass', 'sum', 'twopisum',
         'minimum', 'maximum', 'volume', 'volume_average', 'volume_integral']

    _child_classes = dict(
        mass_average=mass_average_cls,
        mass_integral=mass_integral_cls,
        mass=mass_cls,
        sum=sum_cls,
        twopisum=twopisum_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
        volume=volume_cls,
        volume_average=volume_average_cls,
        volume_integral=volume_integral_cls,
    )

