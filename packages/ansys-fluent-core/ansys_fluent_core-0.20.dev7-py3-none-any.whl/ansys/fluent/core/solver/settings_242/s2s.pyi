#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class s2s:
    fluent_name = ...
    child_names = ...
    viewfactor_settings = ...
    clustering_settings = ...
    radiosity_solver_control = ...
    command_names = ...

    def compute_write_vf(self, file_name: str):
        """
        Compute and write both surface clusters and view factors.
        
        Parameters
        ----------
            file_name : str
                Name of output file for updated surface clusters and view factors.
        
        """

    def compute_vf_accelerated(self, file_name: str):
        """
        Compute and write only view factors from existing surface clusters with GPU-acceleration.
        
        Parameters
        ----------
            file_name : str
                Name of output file for S2S view factors from existing surface clusters with GPU-acceleration.
        
        """

    def compute_clusters_and_vf_accelerated(self, file_name: str):
        """
        Compute and write both surface clusters and view factors with GPU-acceleration.
        
        Parameters
        ----------
            file_name : str
                Name of output file for updated surface clusters and view factors with GPU-acceleration.
        
        """

    def compute_vf_only(self, file_name: str):
        """
        Compute and write only view factors from existing surface clusters.
        
        Parameters
        ----------
            file_name : str
                Name of output file for S2S view factors from existing surface clusters.
        
        """

    def read_vf_file(self, file_name_1: str):
        """
        Read an S2S file.
        
        Parameters
        ----------
            file_name_1 : str
                Name of input file containing view factors.
        
        """

