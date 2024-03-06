#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class discrete_phase:
    fluent_name = ...
    child_names = ...
    histogram = ...
    sample_trajectories = ...
    evap_mass_details_in_dpm_summ_rep = ...
    command_names = ...

    def summary(self, ):
        """
        Print discrete phase summary report of particle fates.
        """

    def extended_summary(self, write_to_file: bool, file_name: str, include_in_domains_particles: bool, pick_injection: bool, injection: str):
        """
        Print extended discrete phase summary report of particle fates, with options.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            include_in_domains_particles : bool
                'include_in_domains_particles' child.
            pick_injection : bool
                'pick_injection' child.
            injection : str
                'injection' child.
        
        """

    def zone_summaries_per_injection(self, summary_state: bool, reset_dpm_summaries: bool):
        """
        Enable per-injection per-zone DPM summary reports.
        
        Parameters
        ----------
            summary_state : bool
                'summary_state' child.
            reset_dpm_summaries : bool
                'reset_dpm_summaries' child.
        
        """

