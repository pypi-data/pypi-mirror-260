#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class mesh_interfaces:
    fluent_name = ...
    child_names = ...
    interface = ...
    auto_options = ...
    turbo_interface = ...
    verbosity = ...
    enforce_continuity_after_bc = ...
    coupled_interfaces_inherit_bcs = ...
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
                Mesh interface name to be deleted.
        
        """

    def list(self, ):
        """
        List all mesh-interfaces.
        """

    def delete_all(self, ):
        """
        Delete all mesh interfaces.
        """

    def display(self, zones: List[str]):
        """
        Display specified mesh interface zone.
        
        Parameters
        ----------
            zones : typing.List[str]
                Zone-name to be displayed.
        
        """

    def one_to_one_pairing(self, one_to_one_interface: bool, proceed: bool, delete_empty: bool):
        """
        Use the default one-to-one interface creation method?.
        
        Parameters
        ----------
            one_to_one_interface : bool
                Use the default one-to-one interface creation method?.
            proceed : bool
                Would you like to proceed?.
            delete_empty : bool
                Delete empty interface interior zones from non-overlapping interfaces?.
        
        """

    def delete_interfaces_with_small_overlap(self, delete: bool, overlapping_percentage_threshold: Union[float, str]):
        """
        Delete mesh interfaces that have an area percentage under a specified value.
        
        Parameters
        ----------
            delete : bool
                Delete mesh interfaces that have an area percentage under a specified value?.
            overlapping_percentage_threshold : real
                Enter the area percentage used for deletion (%).
        
        """

    def create_manually(self, name: str, zone_list_1: List[str], zone_list_2: List[str]):
        """
        Create one-to-one interfaces between two groups of boundary zones even if they do not currently overlap.
        
        Parameters
        ----------
            name : str
                Enter a prefix for mesh interface names.
            zone_list_1 : typing.List[str]
                Enter the boundary zones belonging to the first group.
            zone_list_2 : typing.List[str]
                Enter the boundary zones belonging to the second group.
        
        """

    def auto_pairing(self, pair_all: bool, one_to_one_pairs: bool, interface_zones: List[str], create: bool, name: str, apply_mapped: bool, static_interface: bool):
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

    def improve_quality(self, check_mapped_interface_quality: bool, proceed: bool, tol_percentage_increment: Union[float, str]):
        """
        Improve mesh interface quality.
        
        Parameters
        ----------
            check_mapped_interface_quality : bool
                Check Mapped Interface Qaulity.
            proceed : bool
                Continue to improve the mapped interface quality.
            tol_percentage_increment : real
                Enter a percentage increment for tolerance (%).
        
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
                Enter rotation angle.
            interface_name : str
                Enter a name for this phaselag interface.
        
        """

    def make_phaselag_from_periodic(self, periodic_zone_name: str):
        """
        Convert periodic interface to phase lagged.
        
        Parameters
        ----------
            periodic_zone_name : str
                Enter periodic zone id/name.
        
        """

    def transfer_motion_across_interfaces(self, enabled: bool, option_name: str):
        """
        Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
        
        Parameters
        ----------
            enabled : bool
                Enable motion transfer across mesh interfaces?.
            option_name : str
                Enter transfer type.
        
        """

    def remove_left_handed_interface_faces(self, enable: bool, update: bool):
        """
        Remove left-handed faces during mesh interface creation.
        
        Parameters
        ----------
            enable : bool
                Remove left-handed faces on mesh interfaces.
            update : bool
                Update existing mesh interfaces?.
        
        """

    def non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Enter zone id/name.
        
        """

