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

from .contact_face import contact_face as contact_face_cls
from .resistance_value import resistance_value as resistance_value_cls
class add_contact_resistance(Command):
    """
    'add_contact_resistance' command.
    
    Parameters
    ----------
        contact_face : str
            Set contact face.
        resistance_value : real
            Set resistance value.
    
    """

    fluent_name = "add-contact-resistance"

    argument_names = \
        ['contact_face', 'resistance_value']

    _child_classes = dict(
        contact_face=contact_face_cls,
        resistance_value=resistance_value_cls,
    )

