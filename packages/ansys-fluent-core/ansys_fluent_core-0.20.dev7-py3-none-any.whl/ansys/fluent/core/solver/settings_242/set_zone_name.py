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

from .zonename import zonename as zonename_cls
from .newname import newname as newname_cls
class set_zone_name(Command):
    """
    Give a zone a new name.
    
    Parameters
    ----------
        zonename : str
            Enter a zone name.
        newname : str
            Give a new zone name.
    
    """

    fluent_name = "set-zone-name"

    argument_names = \
        ['zonename', 'newname']

    _child_classes = dict(
        zonename=zonename_cls,
        newname=newname_cls,
    )

