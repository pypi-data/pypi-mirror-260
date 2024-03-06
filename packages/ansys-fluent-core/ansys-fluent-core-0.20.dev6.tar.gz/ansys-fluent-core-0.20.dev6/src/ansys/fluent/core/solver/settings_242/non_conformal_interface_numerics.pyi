#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class non_conformal_interface_numerics:
    fluent_name = ...
    command_names = ...

    def change_numerics(self, use_sided_area_vector: bool, use_nci_sided_area_vectors: bool, recreate: bool):
        """
        Enable modified non-conformal interface numerics.
        
        Parameters
        ----------
            use_sided_area_vector : bool
                Enforce watertight cells for fluid-solid and solid-solid interfaces?.
            use_nci_sided_area_vectors : bool
                Use enhanced gradient computations for fluid-solid and solid-solid interfaces?.
            recreate : bool
                Recreate non-conformal interfaces?.
        
        """

