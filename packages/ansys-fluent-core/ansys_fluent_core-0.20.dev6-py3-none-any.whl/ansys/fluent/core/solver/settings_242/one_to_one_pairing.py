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

from .one_to_one_interface import one_to_one_interface as one_to_one_interface_cls
from .proceed import proceed as proceed_cls
from .delete_empty import delete_empty as delete_empty_cls
class one_to_one_pairing(Command):
    """
    Use the default one-to-one interface creation method?.
    
    Parameters
    ----------
        one_to_one_interface : bool
            Use the default one-to-one interface creation method?.
        proceed : bool
            Would you like to proceed?.
        delete_empty : bool
            Delete empty interface interior zones from non-overlapping interfaces?.
    
    """

    fluent_name = "one-to-one-pairing?"

    argument_names = \
        ['one_to_one_interface', 'proceed', 'delete_empty']

    _child_classes = dict(
        one_to_one_interface=one_to_one_interface_cls,
        proceed=proceed_cls,
        delete_empty=delete_empty_cls,
    )

