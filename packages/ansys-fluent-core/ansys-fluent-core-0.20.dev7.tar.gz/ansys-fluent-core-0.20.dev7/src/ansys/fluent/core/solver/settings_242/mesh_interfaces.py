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

from .interface_2 import interface as interface_cls
from .auto_options import auto_options as auto_options_cls
from .turbo_interface import turbo_interface as turbo_interface_cls
from .verbosity_7 import verbosity as verbosity_cls
from .enforce_continuity_after_bc import enforce_continuity_after_bc as enforce_continuity_after_bc_cls
from .coupled_interfaces_inherit_bcs import coupled_interfaces_inherit_bcs as coupled_interfaces_inherit_bcs_cls
from .enable_si_with_nodes import enable_si_with_nodes as enable_si_with_nodes_cls
from .enforce_coupled_wall_between_solids import enforce_coupled_wall_between_solids as enforce_coupled_wall_between_solids_cls
from .enable_visualization_of_interfaces import enable_visualization_of_interfaces as enable_visualization_of_interfaces_cls
from .mapped_interface_options import mapped_interface_options as mapped_interface_options_cls
from .non_conformal_interface_numerics import non_conformal_interface_numerics as non_conformal_interface_numerics_cls
from .delete_2 import delete as delete_cls
from .list_1 import list as list_cls
from .delete_all import delete_all as delete_all_cls
from .display_1 import display as display_cls
from .one_to_one_pairing import one_to_one_pairing as one_to_one_pairing_cls
from .delete_interfaces_with_small_overlap import delete_interfaces_with_small_overlap as delete_interfaces_with_small_overlap_cls
from .create_manually import create_manually as create_manually_cls
from .auto_pairing import auto_pairing as auto_pairing_cls
from .improve_quality_1 import improve_quality as improve_quality_cls
from .make_phaselag_from_boundaries import make_phaselag_from_boundaries as make_phaselag_from_boundaries_cls
from .make_phaselag_from_periodic import make_phaselag_from_periodic as make_phaselag_from_periodic_cls
from .transfer_motion_across_interfaces import transfer_motion_across_interfaces as transfer_motion_across_interfaces_cls
from .remove_left_handed_interface_faces import remove_left_handed_interface_faces as remove_left_handed_interface_faces_cls
from .non_overlapping_zone_name_1 import non_overlapping_zone_name as non_overlapping_zone_name_cls
class mesh_interfaces(Group):
    """
    Enter the mesh interfaces menu.
    """

    fluent_name = "mesh-interfaces"

    child_names = \
        ['interface', 'auto_options', 'turbo_interface', 'verbosity',
         'enforce_continuity_after_bc', 'coupled_interfaces_inherit_bcs',
         'enable_si_with_nodes', 'enforce_coupled_wall_between_solids',
         'enable_visualization_of_interfaces', 'mapped_interface_options',
         'non_conformal_interface_numerics']

    command_names = \
        ['delete', 'list', 'delete_all', 'display', 'one_to_one_pairing',
         'delete_interfaces_with_small_overlap', 'create_manually',
         'auto_pairing', 'improve_quality', 'make_phaselag_from_boundaries',
         'make_phaselag_from_periodic', 'transfer_motion_across_interfaces',
         'remove_left_handed_interface_faces', 'non_overlapping_zone_name']

    _child_classes = dict(
        interface=interface_cls,
        auto_options=auto_options_cls,
        turbo_interface=turbo_interface_cls,
        verbosity=verbosity_cls,
        enforce_continuity_after_bc=enforce_continuity_after_bc_cls,
        coupled_interfaces_inherit_bcs=coupled_interfaces_inherit_bcs_cls,
        enable_si_with_nodes=enable_si_with_nodes_cls,
        enforce_coupled_wall_between_solids=enforce_coupled_wall_between_solids_cls,
        enable_visualization_of_interfaces=enable_visualization_of_interfaces_cls,
        mapped_interface_options=mapped_interface_options_cls,
        non_conformal_interface_numerics=non_conformal_interface_numerics_cls,
        delete=delete_cls,
        list=list_cls,
        delete_all=delete_all_cls,
        display=display_cls,
        one_to_one_pairing=one_to_one_pairing_cls,
        delete_interfaces_with_small_overlap=delete_interfaces_with_small_overlap_cls,
        create_manually=create_manually_cls,
        auto_pairing=auto_pairing_cls,
        improve_quality=improve_quality_cls,
        make_phaselag_from_boundaries=make_phaselag_from_boundaries_cls,
        make_phaselag_from_periodic=make_phaselag_from_periodic_cls,
        transfer_motion_across_interfaces=transfer_motion_across_interfaces_cls,
        remove_left_handed_interface_faces=remove_left_handed_interface_faces_cls,
        non_overlapping_zone_name=non_overlapping_zone_name_cls,
    )

