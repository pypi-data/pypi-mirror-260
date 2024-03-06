#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class fluxes:
    fluent_name = ...
    command_names = ...

    def mass_flow(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass flow rate at inlets and outlets.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def heat_transfer(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def heat_transfer_sensible(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sensible heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def radiation_heat_transfer(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print radiation heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def film_mass_flow(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print film mass flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def film_heat_transfer(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print film heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def electric_current(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print electric current rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def pressure_work(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print pressure work rate at moving boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def viscous_work(self, domain: str, all_boundary_zones: bool, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print viscous work rate at boundaries.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            all_boundary_zones : bool
                Select all the boundary/interior zones.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

