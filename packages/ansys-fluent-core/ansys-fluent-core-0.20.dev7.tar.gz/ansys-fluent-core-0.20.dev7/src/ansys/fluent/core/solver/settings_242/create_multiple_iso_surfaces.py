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

from .field_1 import field as field_cls
from .name_4 import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .zones_4 import zones as zones_cls
from .min_4 import min as min_cls
from .max_4 import max as max_cls
from .iso_value import iso_value as iso_value_cls
from .no_of_surfaces import no_of_surfaces as no_of_surfaces_cls
from .spacing import spacing as spacing_cls
class create_multiple_iso_surfaces(Command):
    """
    'create_multiple_iso_surfaces' command.
    
    Parameters
    ----------
        field : str
            Specify Field.
        name : str
            'name' child.
        surfaces : typing.List[str]
            Select surface.
        zones : typing.List[str]
            Enter cell zone name list.
        min : real
            Set min.
        max : real
            Set max.
        iso_value : real
            'iso_value' child.
        no_of_surfaces : int
            'no_of_surfaces' child.
        spacing : real
            'spacing' child.
    
    """

    fluent_name = "create-multiple-iso-surfaces"

    argument_names = \
        ['field', 'name', 'surfaces', 'zones', 'min', 'max', 'iso_value',
         'no_of_surfaces', 'spacing']

    _child_classes = dict(
        field=field_cls,
        name=name_cls,
        surfaces=surfaces_cls,
        zones=zones_cls,
        min=min_cls,
        max=max_cls,
        iso_value=iso_value_cls,
        no_of_surfaces=no_of_surfaces_cls,
        spacing=spacing_cls,
    )

