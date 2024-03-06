#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class surfaces:
    fluent_name = ...
    child_names = ...
    point_surface = ...
    line_surface = ...
    rake_surface = ...
    plane_surface = ...
    iso_surface = ...
    iso_clip = ...
    zone_surface = ...
    partition_surface = ...
    transform_surface = ...
    imprint_surface = ...
    plane_slice = ...
    sphere_slice = ...
    quadric_surface = ...
    surface_cells = ...
    command_names = ...

    def create_multiple_zone_surfaces(self, zone_names: List[str]):
        """
        'create_multiple_zone_surfaces' command.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Enter zone name list.
        
        """

    def create_multiple_iso_surfaces(self, field: str, name: str, surfaces: List[str], zones: List[str], iso_value: Union[float, str], no_of_surfaces: int, spacing: Union[float, str]):
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
            iso_value : real
                'iso_value' child.
            no_of_surfaces : int
                'no_of_surfaces' child.
            spacing : real
                'spacing' child.
        
        """

    def create_group_surfaces(self, surfaces: List[str], name: str):
        """
        'create_group_surfaces' command.
        
        Parameters
        ----------
            surfaces : typing.List[str]
                Select list of surfaces.
            name : str
                'name' child.
        
        """

    def ungroup_surfaces(self, surface: str):
        """
        'ungroup_surfaces' command.
        
        Parameters
        ----------
            surface : str
                'surface' child.
        
        """

    def set_rendering_priority(self, surface: str, priority: str):
        """
        'set_rendering_priority' command.
        
        Parameters
        ----------
            surface : str
                Select surface.
            priority : str
                Select surface.
        
        """

    def reset_zone_surfaces(self, ):
        """
        'reset_zone_surfaces' command.
        """

