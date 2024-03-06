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

from .domain import domain as domain_cls
class species_mass_flow(Command):
    """
    'species_mass_flow' command.
    
    Parameters
    ----------
        domain : str
            'domain' child.
    
    """

    fluent_name = "species-mass-flow"

    argument_names = \
        ['domain']

    _child_classes = dict(
        domain=domain_cls,
    )

