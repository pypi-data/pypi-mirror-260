#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class sample_trajectories:
    fluent_name = ...
    child_names = ...
    user_defined_functions = ...
    sort_sample_files = ...
    command_names = ...

    def compute(self, injections: List[str], boundaries: List[str], lines: List[str], planes: List[str], op_udf: str, append_sample: bool, accumulate_rates: bool):
        """
        'compute' command.
        
        Parameters
        ----------
            injections : typing.List[str]
                'injections' child.
            boundaries : typing.List[str]
                'boundaries' child.
            lines : typing.List[str]
                Select surface.
            planes : typing.List[str]
                Select surface.
            op_udf : str
                'op_udf' child.
            append_sample : bool
                'append_sample' child.
            accumulate_rates : bool
                'accumulate_rates' child.
        
        """

    def start_file_write(self, injections: List[str], boundaries: List[str], lines: List[str], planes: List[str], op_udf: str, append_sample: bool, accumulate_rates: bool):
        """
        'start_file_write' command.
        
        Parameters
        ----------
            injections : typing.List[str]
                'injections' child.
            boundaries : typing.List[str]
                'boundaries' child.
            lines : typing.List[str]
                Select surface.
            planes : typing.List[str]
                Select surface.
            op_udf : str
                'op_udf' child.
            append_sample : bool
                'append_sample' child.
            accumulate_rates : bool
                'accumulate_rates' child.
        
        """

    def stop_file_write(self, ):
        """
        'stop_file_write' command.
        """

