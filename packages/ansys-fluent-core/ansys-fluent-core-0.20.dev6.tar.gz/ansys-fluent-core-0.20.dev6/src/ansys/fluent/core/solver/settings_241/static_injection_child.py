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

from .mass_flow_rate_2 import mass_flow_rate as mass_flow_rate_cls
from .flow_direction_1 import flow_direction as flow_direction_cls
from .temperature_3 import temperature as temperature_cls
from .mixture_fraction_2 import mixture_fraction as mixture_fraction_cls
from .progress_variable_2 import progress_variable as progress_variable_cls
from .species_10 import species as species_cls
class static_injection_child(Group):
    """
    'child_object_type' of static_injection.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['mass_flow_rate', 'flow_direction', 'temperature',
         'mixture_fraction', 'progress_variable', 'species']

    _child_classes = dict(
        mass_flow_rate=mass_flow_rate_cls,
        flow_direction=flow_direction_cls,
        temperature=temperature_cls,
        mixture_fraction=mixture_fraction_cls,
        progress_variable=progress_variable_cls,
        species=species_cls,
    )

