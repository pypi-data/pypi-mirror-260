#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class boundary_conditions:
    fluent_name = ...
    child_names = ...
    axis = ...
    degassing = ...
    exhaust_fan = ...
    fan = ...
    geometry = ...
    inlet_vent = ...
    intake_fan = ...
    interface = ...
    interior = ...
    mass_flow_inlet = ...
    mass_flow_outlet = ...
    network = ...
    network_end = ...
    outflow = ...
    outlet_vent = ...
    overset = ...
    periodic = ...
    porous_jump = ...
    pressure_far_field = ...
    pressure_inlet = ...
    pressure_outlet = ...
    radiator = ...
    rans_les_interface = ...
    recirculation_inlet = ...
    recirculation_outlet = ...
    shadow = ...
    symmetry = ...
    velocity_inlet = ...
    wall = ...
    non_reflecting_bc = ...
    perforated_wall = ...
    settings = ...
    command_names = ...

    def copy(self, from_: str, to: List[str], verbosity: bool):
        """
        'copy' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : typing.List[str]
                'to' child.
            verbosity : bool
                'verbosity' child.
        
        """

    def set_zone_type(self, zone_list: List[str], new_type: str):
        """
        'set_zone_type' command.
        
        Parameters
        ----------
            zone_list : typing.List[str]
                Enter zone name list.
            new_type : str
                'new_type' child.
        
        """

    def slit_face_zone(self, zone_name: str):
        """
        Slit a two-sided wall into two connected wall zones.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
        
        """

    def non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
        
        """

    def slit_interior_between_diff_solids(self, ):
        """
        Slit interior created between different solids into coupled walls.
        """

    def create_all_shell_threads(self, ):
        """
        Mark all finite thickness wall for shell creation. Shell zones will be created at the start of iterations.
        """

    def recreate_all_shells(self, ):
        """
        Create shell on all the walls where which were deleted using the command delete-all-shells.
        """

    def delete_all_shells(self, ):
        """
        'delete_all_shells' command.
        """

    def orient_face_zone(self, zone_name: str):
        """
        Orient the face zone.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
        
        """

    def knudsen_number_calculator(self, length: Union[float, str], boundary: str):
        """
        Utility to compute Kudsen number based on characteristic length and boundary information.
        
        Parameters
        ----------
            length : real
                Characteristic physics length.
            boundary : str
                'boundary' child.
        
        """

    def set_zone_name(self, zonename: str, newname: str):
        """
        Give a zone a new name.
        
        Parameters
        ----------
            zonename : str
                Enter a zone name.
            newname : str
                'newname' child.
        
        """

    def add_suffix_or_prefix(self, zone_name: List[str], append: bool, text: str):
        """
        Add suffix or prefix to zone name.
        
        Parameters
        ----------
            zone_name : typing.List[str]
                Enter zone name list.
            append : bool
                'append' child.
            text : str
                'text' child.
        
        """

    def rename_by_adjacency(self, zone_name: List[str], abbreviate_types: bool, exclude: bool):
        """
        Rename zone to adjacent zones.
        
        Parameters
        ----------
            zone_name : typing.List[str]
                Enter zone name list.
            abbreviate_types : bool
                'abbreviate_types' child.
            exclude : bool
                'exclude' child.
        
        """

    def rename_to_default(self, zone_name: List[str], abbrev: bool, exclude: bool):
        """
        Rename zone to default name.
        
        Parameters
        ----------
            zone_name : typing.List[str]
                Enter zone name list.
            abbrev : bool
                'abbrev' child.
            exclude : bool
                'exclude' child.
        
        """

