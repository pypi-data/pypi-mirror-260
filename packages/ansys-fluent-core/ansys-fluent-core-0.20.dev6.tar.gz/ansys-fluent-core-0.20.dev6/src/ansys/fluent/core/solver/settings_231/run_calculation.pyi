#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class run_calculation:
    fluent_name = ...
    child_names = ...
    adaptive_time_stepping = ...
    cfl_based_adaptive_time_stepping = ...
    data_sampling = ...
    transient_controls = ...
    pseudo_time_settings = ...
    data_sampling_options = ...
    iter_count = ...
    reporting_interval = ...
    residual_verbosity = ...
    time_step_count = ...
    command_names = ...

    def dual_time_iterate(self, total_period_count: int, time_step_count: int, total_time_step_count: int, total_time: Union[float, str], incremental_time: Union[float, str], max_iter_per_step: int, postprocess: bool, post_iter_per_time_step_count: int):
        """
        Perform unsteady iterations.
        
        Parameters
        ----------
            total_period_count : int
                Set number of total periods.
            time_step_count : int
                Set inceremtal number of Time steps.
            total_time_step_count : int
                Set total number of Time steps.
            total_time : real
                Set Total Simulation Time.
            incremental_time : real
                Set Incremental Time.
            max_iter_per_step : int
                Set Maximum Number of iterations per time step.
            postprocess : bool
                Enable/Disable Postprocess pollutant solution?.
            post_iter_per_time_step_count : int
                Set Number of post-processing iterations per time step.
        
        """

    def iterate(self, iter_count: int):
        """
        Perform a specified number of iterations.
        
        Parameters
        ----------
            iter_count : int
                Set incremental number of time steps.
        
        """

    def calculate(self, ):
        """
        'calculate' command.
        """

    def interrupt(self, end_of_timestep: bool):
        """
        Interrupt the iterations.
        
        Parameters
        ----------
            end_of_timestep : bool
                'end_of_timestep' child.
        
        """

    query_names = ...

    def iterating(self, ):
        """
        'iterating' query.
        """

