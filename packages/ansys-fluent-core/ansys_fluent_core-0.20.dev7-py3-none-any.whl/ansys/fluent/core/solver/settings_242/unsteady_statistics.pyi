#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class unsteady_statistics:
    fluent_name = ...
    command_names = ...

    def sc_enable_sub_stepping_option_per_coupling_step(self, enable_sub_stepping: bool, num_sub_stepping_coupling_itr: int):
        """
        Enable/disable sub stepping option per coupling step.
        
        Parameters
        ----------
            enable_sub_stepping : bool
                Enable or Disable sub stepping options for each coupling  steps.
            num_sub_stepping_coupling_itr : int
                Set the number of substeps for each coupling iterations (default = 1).
        
        """

