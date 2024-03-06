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

from .zone_name_8 import zone_name as zone_name_cls
from .append import append as append_cls
from .text import text as text_cls
class add_suffix_or_prefix(Command):
    """
    Add suffix or prefix to zone name.
    
    Parameters
    ----------
        zone_name : typing.List[str]
            Enter zone name list.
        append : bool
            Add suffix to zone name.
        text : str
            Add prefix to zone name.
    
    """

    fluent_name = "add-suffix-or-prefix"

    argument_names = \
        ['zone_name', 'append', 'text']

    _child_classes = dict(
        zone_name=zone_name_cls,
        append=append_cls,
        text=text_cls,
    )

