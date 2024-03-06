#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class number_of_bands:
    fluent_name = ...
    command_names = ...

    def on_all_interfaces(self, bands: int):
        """
        Maximum number of bands to be employed at all the mixing planes.
        
        Parameters
        ----------
            bands : int
                Maximum number of band counts.
        
        """

    def on_specified_interface(self, interface_name: str, bands: int):
        """
        Maximum number of bands to be employed at the specified mixing plane interface.
        
        Parameters
        ----------
            interface_name : str
                Define the mixing plane interface to specify band count.
            bands : int
                Maximum number of band counts.
        
        """

