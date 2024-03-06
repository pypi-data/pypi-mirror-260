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

from .zone_name_6 import zone_name as zone_name_cls
from .value_7 import value as value_cls
class add_zone(Command):
    """
    Add thread-real-pair object.
    
    Parameters
    ----------
        zone_name : str
            Specify zone name in add-zone operation.
        value : real
            Specify value in add-zone operation.
    
    """

    fluent_name = "add-zone"

    argument_names = \
        ['zone_name', 'value']

    _child_classes = dict(
        zone_name=zone_name_cls,
        value=value_cls,
    )

