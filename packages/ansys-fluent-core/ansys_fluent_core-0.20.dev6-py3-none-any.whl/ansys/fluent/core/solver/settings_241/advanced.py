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
class advanced(Group):
    """
    'advanced' child.
    """

    fluent_name = "advanced"

    child_names = \
        ['contact_resis']

    _child_classes = dict(
        contact_resis=contact_resis_cls,
    )

