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

from .unit_system import unit_system as unit_system_cls
class set_unit_system(Command):
    """
    To apply standard set of units to all quantities.
    
    Parameters
    ----------
        unit_system : str
            'unit_system' child.
    
    """

    fluent_name = "set-unit-system"

    argument_names = \
        ['unit_system']

    _child_classes = dict(
        unit_system=unit_system_cls,
    )

