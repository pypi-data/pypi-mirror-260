#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class report:
    fluent_name = ...
    child_names = ...
    simulation_reports = ...
    discrete_phase = ...
    fluxes = ...
    flow = ...
    modified_setting_options = ...
    population_balance = ...
    heat_exchanger = ...
    system = ...
    surface_integrals = ...
    volume_integrals = ...
    command_names = ...

    def aero_optical_distortions(self, ):
        """
        Optics report menu.
        """

    def forces(self, option: str, domain: str, all_wall_zones: bool, wall_zones: List[str], direction_vector: List[Union[float, str]], momentum_center: List[Union[float, str]], momentum_axis: List[Union[float, str]], pressure_coordinate: str, coordinate_value: Union[float, str], write_to_file: bool, file_name: str, append_data: bool):
        """
        'forces' command.
        
        Parameters
        ----------
            option : str
                'option' child.
            domain : str
                'domain' child.
            all_wall_zones : bool
                Select all wall zones available.
            wall_zones : typing.List[str]
                Enter wall zone name list.
            direction_vector : typing.List[real]
                'direction_vector' child.
            momentum_center : typing.List[real]
                'momentum_center' child.
            momentum_axis : typing.List[real]
                'momentum_axis' child.
            pressure_coordinate : str
                'pressure_coordinate' child.
            coordinate_value : real
                'coordinate_value' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def multiphase_summary(self, verbosity_option: str):
        """
        Multiphase Summary and Recommendations.
        
        Parameters
        ----------
            verbosity_option : str
                'verbosity_option' child.
        
        """

    def particle_summary(self, injection_names: List[str]):
        """
        Print summary report for all current particles.
        
        Parameters
        ----------
            injection_names : typing.List[str]
                'injection_names' child.
        
        """

    def pathline_summary(self, ):
        """
        Print path-line-summary report.
        """

    def projected_surface_area(self, surfaces: List[str], min_feature_size: Union[float, str], proj_plane_norm_comp: List[Union[float, str]]):
        """
        Print total area of the projection of a group of surfaces to a plane.
        
        Parameters
        ----------
            surfaces : typing.List[str]
                Select surface.
            min_feature_size : real
                'min_feature_size' child.
            proj_plane_norm_comp : typing.List[real]
                'proj_plane_norm_comp' child.
        
        """

    def summary(self, write_to_file: bool, file_name: str):
        """
        Print report summary.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
        
        """

    def vbm(self, output_quantity: str, rotor_name: str, scale_output: bool, write_to_file: bool, file_name: str, append: bool):
        """
        'vbm' command.
        
        Parameters
        ----------
            output_quantity : str
                'output_quantity' child.
            rotor_name : str
                'rotor_name' child.
            scale_output : bool
                'scale_output' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append : bool
                'append' child.
        
        """

