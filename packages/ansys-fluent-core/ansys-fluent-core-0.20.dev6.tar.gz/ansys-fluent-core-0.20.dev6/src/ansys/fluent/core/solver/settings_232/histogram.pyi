#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class histogram:
    fluent_name = ...
    child_names = ...
    histogram_options = ...
    histogram_parameters = ...
    plot_write_sample = ...
    reduction = ...
    command_names = ...

    def compute_sample(self, sample: str, variable: str):
        """
        Compute minimum/maximum of a sample variable.
        
        Parameters
        ----------
            sample : str
                'sample' child.
            variable : str
                'variable' child.
        
        """

    def delete_sample(self, sample: str):
        """
        'delete_sample' command.
        
        Parameters
        ----------
            sample : str
                'sample' child.
        
        """

    def list_samples(self, ):
        """
        Show all samples in loaded sample list.
        """

    def read_sample_file(self, sample_file: str):
        """
        Read a sample file and add it to the sample list.
        
        Parameters
        ----------
            sample_file : str
                Enter the name of a sample file to be loaded.
        
        """

    def dpm_sample_contour_plots(self, sample_name: str, interval_size: Union[float, str]):
        """
        Prepare named expressions from data in a DPM sample file (collected at a cut plane surface) for contour plotting.
        
        Parameters
        ----------
            sample_name : str
                'sample_name' child.
            interval_size : real
                'interval_size' child.
        
        """

