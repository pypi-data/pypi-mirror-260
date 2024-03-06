#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class data_sampling_options:
    fluent_name = ...
    child_names = ...
    data_sets = ...
    command_names = ...

    def add_datasets(self, zone_names: List[str], domain: str, quantities: List[str], min: bool, max: bool, mean: bool, rmse: bool, moving_average: bool, average_over: int):
        """
        Add datasets.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Enter zone name list.
            domain : str
                'domain' child.
            quantities : typing.List[str]
                'quantities' child.
            min : bool
                'min' child.
            max : bool
                'max' child.
            mean : bool
                'mean' child.
            rmse : bool
                'rmse' child.
            moving_average : bool
                'moving_average' child.
            average_over : int
                'average_over' child.
        
        """

    def list_datasets(self, ):
        """
        List dataset.
        """

