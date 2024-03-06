#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class by_surface:
    fluent_name = ...
    child_names = ...
    use_inherent_material_color = ...
    command_names = ...

    def reset(self, ):
        """
        To reset colors and/or materials to the defaults.
        """

    def list_surfaces_by_color(self, ):
        """
        To list the surfaces by its color.
        """

    def list_surfaces_by_material(self, ):
        """
        To list the surfaces by its material.
        """

    def surfaces(self, surface_names: List[str], color: str, material: str):
        """
        Select the surface(s) to specify colors and/or materials.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Enter the list of surfaces to set color and material.
            color : str
                'color' child.
            material : str
                'material' child.
        
        """

