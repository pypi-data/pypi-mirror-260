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

from .option_11 import option as option_cls
from .change_all_one_to_one_interfaces_names import change_all_one_to_one_interfaces_names as change_all_one_to_one_interfaces_names_cls
class naming_option(Command):
    """
    Specify whether or not to include an informative suffix to the mesh interface name.
    
    Parameters
    ----------
        option : str
            (0) basic:           name-prefix:##
    (1) name-based:      name-prefix:##:interface_name1::interface_name2
    (2) ID-based:        name-prefix:##:interface_ID1::interface-ID2
    (3) adjacency-based: name-prefix:##:cell_zone_name1::cell_zone_name2.
        change_all_one_to_one_interfaces_names : bool
            Apply the new naming option to existing one-to-one mesh interfaces?.
    
    """

    fluent_name = "naming-option"

    argument_names = \
        ['option', 'change_all_one_to_one_interfaces_names']

    _child_classes = dict(
        option=option_cls,
        change_all_one_to_one_interfaces_names=change_all_one_to_one_interfaces_names_cls,
    )

