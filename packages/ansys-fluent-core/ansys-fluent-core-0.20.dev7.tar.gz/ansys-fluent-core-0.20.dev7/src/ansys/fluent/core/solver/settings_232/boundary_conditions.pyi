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

    def change_type(self, zone_list: List[str], new_type: str):
        """
        'change_type' command.
        
        Parameters
        ----------
            zone_list : typing.List[str]
                'zone_list' child.
            new_type : str
                'new_type' child.
        
        """

    def slit_face_zone(self, zone_id: int):
        """
        Slit a two-sided wall into two connected wall zones.
        
        Parameters
        ----------
            zone_id : int
                'zone_id' child.
        
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

    def orient_face_zone(self, face_zone_id: int):
        """
        Orient the face zone.
        
        Parameters
        ----------
            face_zone_id : int
                'face_zone_id' child.
        
        """

