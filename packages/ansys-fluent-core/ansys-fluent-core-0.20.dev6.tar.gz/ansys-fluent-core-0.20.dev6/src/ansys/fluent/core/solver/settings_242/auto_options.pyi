#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class auto_options:
    fluent_name = ...
    child_names = ...
    proximity_tolerance = ...
    set_default_name_prefix = ...
    set_one_to_one_pairing_tolerance = ...
    set_minimum_area_percentage = ...
    pairing_between_different_cell_zones_only = ...
    pairing_between_interface_zones_only = ...
    keep_empty_interface = ...
    command_names = ...

    def naming_option(self, option: str, change_all_one_to_one_interfaces_names: bool):
        """
        Specify whether or not to include an informative suffix to the mesh interface name.
        
        Parameters
        ----------
            option : str
                (0) basic:           name-prefix:##
        (1) name-based:      name-prefix:##:interface_name1::interface_name2
        (2) ID-based:        name-prefix:##:interface_ID1::interface-ID2
        (3) adjacency-based: name-prefix:##:cell_zone_name1::cell_zone_name2.
            change_all_one_to_one_interfaces_names : bool
                Apply the new naming option to existing one-to-one mesh interfaces?.
        
        """

