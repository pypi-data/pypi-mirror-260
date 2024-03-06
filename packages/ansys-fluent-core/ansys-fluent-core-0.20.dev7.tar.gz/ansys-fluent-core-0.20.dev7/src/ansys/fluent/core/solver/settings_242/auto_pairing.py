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

from .pair_all import pair_all as pair_all_cls
from .one_to_one_pairs import one_to_one_pairs as one_to_one_pairs_cls
from .interface_zones import interface_zones as interface_zones_cls
from .create_2 import create as create_cls
from .name_2 import name as name_cls
from .apply_mapped import apply_mapped as apply_mapped_cls
from .static_interface import static_interface as static_interface_cls
class auto_pairing(Command):
    """
    Automatically pair and create mesh interfaces for some or all interface zones.
    
    Parameters
    ----------
        pair_all : bool
            Automatic pairing of all unintersected interface zones?.
        one_to_one_pairs : bool
            Create one-to-one pairs only?.
        interface_zones : typing.List[str]
            Select unintersected interface zones for pairing.
        create : bool
            Create mesh interfaces with all these pairs?.
        name : str
            Enter a prefix for mesh interface names.
        apply_mapped : bool
            Apply Mapped option at solids.
        static_interface : bool
            Static?.
    
    """

    fluent_name = "auto-pairing"

    argument_names = \
        ['pair_all', 'one_to_one_pairs', 'interface_zones', 'create', 'name',
         'apply_mapped', 'static_interface']

    _child_classes = dict(
        pair_all=pair_all_cls,
        one_to_one_pairs=one_to_one_pairs_cls,
        interface_zones=interface_zones_cls,
        create=create_cls,
        name=name_cls,
        apply_mapped=apply_mapped_cls,
        static_interface=static_interface_cls,
    )

