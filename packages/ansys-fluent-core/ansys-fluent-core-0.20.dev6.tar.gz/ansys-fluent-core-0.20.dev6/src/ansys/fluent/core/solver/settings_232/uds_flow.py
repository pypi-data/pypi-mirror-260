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

from .domain_val import domain_val as domain_val_cls
class uds_flow(Command):
    """
    'uds_flow' command.
    
    Parameters
    ----------
        domain_val : str
            'domain_val' child.
    
    """

    fluent_name = "uds-flow"

    argument_names = \
        ['domain_val']

    _child_classes = dict(
        domain_val=domain_val_cls,
    )

