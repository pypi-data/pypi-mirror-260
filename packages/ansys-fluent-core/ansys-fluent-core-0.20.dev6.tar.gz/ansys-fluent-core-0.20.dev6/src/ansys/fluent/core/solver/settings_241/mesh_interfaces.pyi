#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class mesh_interfaces:
    fluent_name = ...
    child_names = ...
    auto_options = ...
    interface = ...
    turbo_interface = ...
    enforce_continuity_after_bc = ...
    coupled_interfaces_inherit_bcs = ...
    verbosity = ...
    enable_si_with_nodes = ...
    enforce_coupled_wall_between_solids = ...
    enable_visualization_of_interfaces = ...
    mapped_interface_options = ...
    non_conformal_interface_numerics = ...
    command_names = ...

    def delete(self, name: str):
        """
        Delete a mesh interface.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def display(self, zones: List[str]):
        """
        Display specified mesh interface zone.
        
        Parameters
        ----------
            zones : typing.List[str]
                Enter zone name list.
        
        """

    def list(self, ):
        """
        List all mesh-interfaces.
        """

    def make_phaselag_from_boundaries(self, side_1: str, side_2: str, angle: Union[float, str], interface_name: str):
        """
        Make interface zones phase lagged.
        
        Parameters
        ----------
            side_1 : str
                Enter id/name of zone to convert to phase lag side 1.
            side_2 : str
                Enter id/name of zone to convert to phase lag side 2.
            angle : real
                'angle' child.
            interface_name : str
                'interface_name' child.
        
        """

    def make_phaselag_from_periodic(self, periodic_zone_name: str):
        """
        Convert periodic interface to phase lagged.
        
        Parameters
        ----------
            periodic_zone_name : str
                Enter a periodic zone name.
        
        """

    def delete_interfaces_with_small_overlap(self, delete: bool, overlapping_percentage_threshold: Union[float, str]):
        """
        Delete mesh interfaces that have an area percentage under a specified value.
        
        Parameters
        ----------
            delete : bool
                'delete' child.
            overlapping_percentage_threshold : real
                'overlapping_percentage_threshold' child.
        
        """

    def delete_all(self, ):
        """
        Delete all mesh interfaces.
        """

    def improve_quality(self, check_mapped_interface_quality: bool, continue_: bool, tol_percentage_increment: Union[float, str]):
        """
        Improve mesh interface quality.
        
        Parameters
        ----------
            check_mapped_interface_quality : bool
                Check Mapped Interface Qaulity.
            continue_ : bool
                Continue to improve the mapped interface quality.
            tol_percentage_increment : real
                'tol_percentage_increment' child.
        
        """

    def one_to_one_pairing(self, o2o_flag: bool, toggle: bool, delete_empty: bool):
        """
        Use the default one-to-one interface creation method?.
        
        Parameters
        ----------
            o2o_flag : bool
                Use the default one-to-one interface creation method?.
            toggle : bool
                Would you like to proceed?.
            delete_empty : bool
                Delete empty interface interior zones from non-overlapping interfaces?.
        
        """

    def auto_pairing(self, all: bool, one_to_one_pairing: bool, new_interface_zones: List[str], si_create: bool, si_name: str, apply_mapped: bool, static_interface: bool):
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

    def transfer_motion_across_interfaces(self, enabled: bool, option_name: str):
        """
        Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
        
        Parameters
        ----------
            enabled : bool
                'enabled' child.
            option_name : str
                'option_name' child.
        
        """

    def remove_left_handed_interface_faces(self, enable: bool, update: bool):
        """
        Remove left-handed faces during mesh interface creation.
        
        Parameters
        ----------
            enable : bool
                Remove left-handed faces on mesh interfaces.
            update : bool
                'update' child.
        
        """

    def non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Enter zone id/name.
        
        """

