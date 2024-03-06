#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class mapped_interface_options:
    fluent_name = ...
    command_names = ...

    def solution_controls(self, mapping_frequency: int, under_relaxation_factor: Union[float, str]):
        """
        Specification of mapped frequency and under-relaxation factor for mapped interfaces.
        
        Parameters
        ----------
            mapping_frequency : int
                Mapping Frequency.
            under_relaxation_factor : real
                Under-Relaxation Factor.
        
        """

    def tolerance(self, use_local_edge_length_factor: bool, gtol_length_factor: Union[float, str], gtol_absolute_value: Union[float, str], update: bool):
        """
        Specification of mapped interface tolerance.
        
        Parameters
        ----------
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                Tolerance.
            gtol_absolute_value : real
                Tolerance.
            update : bool
                Update mapped interface with new tolerance.
        
        """

    def convert_to_mapped_interface(self, convert_all: bool, convert_poorly_matching: bool, use_local_edge_length_factor: bool, gtol_length_factor: Union[float, str], gtol_absolute_value: Union[float, str]):
        """
        Convert non-conformal mesh interface to mapped mesh interfaces.
        
        Parameters
        ----------
            convert_all : bool
                Convert all mesh interfaces to mapped mesh interfaces.
            convert_poorly_matching : bool
                Convert poorly matching mesh interfaces to mapped mesh interfaces.
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                Tolerance.
            gtol_absolute_value : real
                Tolerance.
        
        """

