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

from .all_1 import all as all_cls
from .one_to_one_pairing_1 import one_to_one_pairing as one_to_one_pairing_cls
from .new_interface_zones import new_interface_zones as new_interface_zones_cls
from .si_create import si_create as si_create_cls
from .si_name import si_name as si_name_cls
from .apply_mapped import apply_mapped as apply_mapped_cls
from .static_interface import static_interface as static_interface_cls
class auto_pairing(Command):
    """
    Automatically pair and create mesh interfaces for some or all interface zones.
    
    Parameters
    ----------
        all : bool
            'all' child.
        one_to_one_pairing : bool
            'one_to_one_pairing' child.
        new_interface_zones : typing.List[str]
            Select unintersected interface zones for pairing.
        si_create : bool
            'si_create' child.
        si_name : str
            Enter a prefix for mesh interface names.
        apply_mapped : bool
            Apply Mapped option at solids.
        static_interface : bool
            'static_interface' child.
    
    """

    fluent_name = "auto-pairing"

    argument_names = \
        ['all', 'one_to_one_pairing', 'new_interface_zones', 'si_create',
         'si_name', 'apply_mapped', 'static_interface']

    _child_classes = dict(
        all=all_cls,
        one_to_one_pairing=one_to_one_pairing_cls,
        new_interface_zones=new_interface_zones_cls,
        si_create=si_create_cls,
        si_name=si_name_cls,
        apply_mapped=apply_mapped_cls,
        static_interface=static_interface_cls,
    )

