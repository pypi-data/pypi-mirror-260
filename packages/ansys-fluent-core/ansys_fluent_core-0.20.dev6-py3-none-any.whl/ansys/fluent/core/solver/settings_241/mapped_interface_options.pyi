#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class mapped_interface_options:
    fluent_name = ...
    command_names = ...

    def solution_controls(self, mf: int, urf: Union[float, str]):
        """
        Specification of mapped frequency and under-relaxation factor for mapped interfaces.
        
        Parameters
        ----------
            mf : int
                'mf' child.
            urf : real
                'urf' child.
        
        """

    def tolerance(self, use_local_edge_length_factor: bool, gtol_length_factor: Union[float, str], gtol_absolute_value: Union[float, str], update: bool):
        """
        Specification of mapped interface tolerance.
        
        Parameters
        ----------
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                'gtol_length_factor' child.
            gtol_absolute_value : real
                'gtol_absolute_value' child.
            update : bool
                Update mapped interface with new tolerance.
        
        """

    def convert_to_mapped_interface(self, all: bool, auto: bool, use_local_edge_length_factor: bool, gtol_length_factor: Union[float, str], gtol_absolute_value: Union[float, str]):
        """
        Convert non-conformal mesh interface to mapped mesh interfaces.
        
        Parameters
        ----------
            all : bool
                Convert all mesh interfaces to mapped mesh interfaces.
            auto : bool
                Convert poorly matching mesh interfaces to mapped mesh interfaces.
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                'gtol_length_factor' child.
            gtol_absolute_value : real
                'gtol_absolute_value' child.
        
        """

