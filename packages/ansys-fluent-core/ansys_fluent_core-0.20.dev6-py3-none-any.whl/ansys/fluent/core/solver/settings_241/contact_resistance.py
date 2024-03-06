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

from .add_contact_resistance import add_contact_resistance as add_contact_resistance_cls
from .list_contact_face import list_contact_face as list_contact_face_cls
from .delete_contact_face import delete_contact_face as delete_contact_face_cls
class contact_resistance(Group):
    """
    'contact_resistance' child.
    """

    fluent_name = "contact-resistance"

    command_names = \
        ['add_contact_resistance', 'list_contact_face', 'delete_contact_face']

    _child_classes = dict(
        add_contact_resistance=add_contact_resistance_cls,
        list_contact_face=list_contact_face_cls,
        delete_contact_face=delete_contact_face_cls,
    )

