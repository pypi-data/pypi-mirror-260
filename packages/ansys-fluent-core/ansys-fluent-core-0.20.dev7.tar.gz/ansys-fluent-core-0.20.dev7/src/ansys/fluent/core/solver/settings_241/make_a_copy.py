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

from .from_ import from_ as from__cls
from .to import to as to_cls
class make_a_copy(Command):
    """
    Create a copy of the object.
    
    Parameters
    ----------
        from_ : str
            Select the object to duplicate.
        to : str
            Specify the name of the new object.
    
    """

    fluent_name = "make-a-copy"

    argument_names = \
        ['from_', 'to']

    _child_classes = dict(
        from_=from__cls,
        to=to_cls,
    )

