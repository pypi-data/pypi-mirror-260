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

from .species_mass_flow import species_mass_flow as species_mass_flow_cls
from .element_mass_flow import element_mass_flow as element_mass_flow_cls
from .uds_flow import uds_flow as uds_flow_cls
class flow(Group):
    """
    'flow' child.
    """

    fluent_name = "flow"

    command_names = \
        ['species_mass_flow', 'element_mass_flow', 'uds_flow']

    _child_classes = dict(
        species_mass_flow=species_mass_flow_cls,
        element_mass_flow=element_mass_flow_cls,
        uds_flow=uds_flow_cls,
    )

