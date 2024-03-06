#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class fmg:
    fluent_name = ...
    child_names = ...
    fmg_courant_number = ...
    enable_fmg_verbose = ...
    viscous_terms = ...
    species_reactions = ...
    turbulent_viscosity_ratio = ...
    command_names = ...

    def fmg_initialize(self, ):
        """
        Initialize using the full-multigrid initialization (FMG).
        """

    def customize(self, multi_level_grid: int, residual_reduction: List[Union[float, str]], cycle_count: List[Union[float, str]]):
        """
        Enter FMG customization menu.
        
        Parameters
        ----------
            multi_level_grid : int
                Enter number of multigrid levels.
            residual_reduction : typing.List[real]
                Enter number of residual reduction levels.
            cycle_count : typing.List[real]
                Enter number of cycles.
        
        """

    def reset_to_defaults(self, ):
        """
        'reset_to_defaults' command.
        """

