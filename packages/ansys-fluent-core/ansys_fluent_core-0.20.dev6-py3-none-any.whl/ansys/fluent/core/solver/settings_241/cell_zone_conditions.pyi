#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class cell_zone_conditions:
    fluent_name = ...
    child_names = ...
    fluid = ...
    solid = ...
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

    def activate_cell_zone(self, cell_zone_list: List[str]):
        """
        Activate a cell thread.
        
        Parameters
        ----------
            cell_zone_list : typing.List[str]
                'cell_zone_list' child.
        
        """

    def mrf_to_sliding_mesh(self, cell_zone_name: str):
        """
        Change motion specification from MRF to moving mesh.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a cell zone name.
        
        """

    def convert_all_solid_mrf_to_solid_motion(self, ):
        """
        Change all solid zones motion specification from MRF to solid motion.
        """

    def copy_mrf_to_mesh_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
            overwrite : bool
                'overwrite' child.
        
        """

    def copy_mesh_to_mrf_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
            overwrite : bool
                'overwrite' child.
        
        """

