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
from .change_all_o2o_si_names import change_all_o2o_si_names as change_all_o2o_si_names_cls
class naming_option(Command):
    """
    Specify whether or not to include an informative suffix to the mesh interface name.
    
    Parameters
    ----------
        option : int
            'option' child.
        change_all_o2o_si_names : bool
            'change_all_o2o_si_names' child.
    
    """

    fluent_name = "naming-option"

    argument_names = \
        ['option', 'change_all_o2o_si_names']

    _child_classes = dict(
        option=option_cls,
        change_all_o2o_si_names=change_all_o2o_si_names_cls,
    )

