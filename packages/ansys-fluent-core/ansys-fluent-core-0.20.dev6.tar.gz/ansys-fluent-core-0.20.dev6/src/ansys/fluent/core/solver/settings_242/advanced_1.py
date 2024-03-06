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

from .contact_resis import contact_resis as contact_resis_cls
from .coolant_channel import coolant_channel as coolant_channel_cls
from .stack_management import stack_management as stack_management_cls
class advanced(Group):
    """
    Advanced settings.
    """

    fluent_name = "advanced"

    child_names = \
        ['contact_resis', 'coolant_channel', 'stack_management']

    _child_classes = dict(
        contact_resis=contact_resis_cls,
        coolant_channel=coolant_channel_cls,
        stack_management=stack_management_cls,
    )

