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
class duplicate(Command):
    """
    'duplicate' command.
    
    Parameters
    ----------
        from_ : str
            'from' child.
        to : str
            'to' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['from_', 'to']

    _child_classes = dict(
        from_=from__cls,
        to=to_cls,
    )

