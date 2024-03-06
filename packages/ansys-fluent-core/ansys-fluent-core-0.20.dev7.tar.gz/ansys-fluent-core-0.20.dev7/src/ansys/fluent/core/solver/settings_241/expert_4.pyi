#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class expert:
    fluent_name = ...
    command_names = ...

    def enforce_flux_scaling(self, enable_scale_all: bool, disable_scale_all: bool, interface_name: str, scale: bool):
        """
        Enforce flux scaling ON/OFF at the turbo interfaces.
        
        Parameters
        ----------
            enable_scale_all : bool
                Scale scaling of all the interfaces...
            disable_scale_all : bool
                Disable scaling of all the interfaces...
            interface_name : str
                'interface_name' child.
            scale : bool
                Enable flux scaling at mixing plane interface.
        
        """

    def print_settings(self, ):
        """
        List the flux scale settings at the turbo interfaces.
        """

