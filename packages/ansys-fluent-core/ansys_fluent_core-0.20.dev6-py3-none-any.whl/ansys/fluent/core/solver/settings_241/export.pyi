#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class export:
    fluent_name = ...
    child_names = ...
    sc_def_file_settings = ...
    settings = ...
    command_names = ...

    def abaqus(self, file_name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an ABAQUS file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surface_name_list : typing.List[str]
                Select surface.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
        
        """

    def mechanical_apdl(self, file_name: str, thread_name_list: List[str]):
        """
        Write an Mechanical APDL file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            thread_name_list : typing.List[str]
                Enter cell zone name list.
        
        """

    def mechanical_apdl_input(self, file_name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an Mechanical APDL Input file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surface_name_list : typing.List[str]
                Select surface.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
        
        """

    def ascii(self, file_name: str, surface_name_list: List[str], delimiter: str, cell_func_domain: List[str], location: str):
        """
        Write an ASCII file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surface_name_list : typing.List[str]
                List of surfaces to export.
            delimiter : str
                'delimiter' child.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
            location : str
                'location' child.
        
        """

    def avs(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write an AVS UCD file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def ensight(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write EnSight 6 geometry, velocity, and scalar files.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def ensight_gold(self, file_name: str, cell_func_domain_export: List[str], binary_format: bool, cellzones: List[str], interior_zone_surfaces: List[str], cell_centered: bool):
        """
        Write EnSight Gold geometry, velocity, and scalar files.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
            binary_format : bool
                'binary_format' child.
            cellzones : typing.List[str]
                List of cell zones to export.
            interior_zone_surfaces : typing.List[str]
                List of surfaces to export.
            cell_centered : bool
                'cell_centered' child.
        
        """

    def fieldview(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def fieldview_data(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def gambit(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write a Gambit neutral file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def cgns(self, file_name: str, scope: str, cell_zones: List[str], surfaces: List[str], cell_centered: bool, format_class: str, cgns_scalar: List[str]):
        """
        Write a CGNS file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            scope : str
                'scope' child.
            cell_zones : typing.List[str]
                Enter cell zone name list.
            surfaces : typing.List[str]
                Select surface.
            cell_centered : bool
                'cell_centered' child.
            format_class : str
                'format_class' child.
            cgns_scalar : typing.List[str]
                'cgns_scalar' child.
        
        """

    def custom_heat_flux(self, file_name: str, wall_function: bool, surface_name_list: List[str]):
        """
        Write a generic file for heat transfer.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            wall_function : bool
                'wall_function' child.
            surface_name_list : typing.List[str]
                Select surface.
        
        """

    def dx(self, file_name: str, surfaces: List[str], techplot_scalars: List[str]):
        """
        Write an IBM Data Explorer format file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                Select surface.
            techplot_scalars : typing.List[str]
                'techplot_scalars' child.
        
        """

    def ensight_gold_parallel_surfaces(self, file_name: str, binary_format: bool, surfaces: List[str], cell_centered: bool, cell_function: List[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            binary_format : bool
                'binary_format' child.
            surfaces : typing.List[str]
                Select surface.
            cell_centered : bool
                'cell_centered' child.
            cell_function : typing.List[str]
                'cell_function' child.
        
        """

    def ensight_gold_parallel_volume(self, file_name: str, binary_format: bool, cellzones: List[str], cell_centered: bool, cell_function: List[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            binary_format : bool
                'binary_format' child.
            cellzones : typing.List[str]
                Enter cell zone name list.
            cell_centered : bool
                'cell_centered' child.
            cell_function : typing.List[str]
                'cell_function' child.
        
        """

    def icemcfd_for_icepak(self, file_name: str):
        """
        Write a binary ICEMCFD domain file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def fast_mesh(self, file_name: str):
        """
        Write a FAST/Plot3D unstructured mesh file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def fast_solution(self, file_name: str):
        """
        Write a FAST/Plot3D unstructured solution file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def fast_velocity(self, file_name: str):
        """
        Write a FAST/Plot3D unstructured vector function file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def taitherm(self, file_name: str, surface_name_list: List[str], wall_function: bool, htc_on_walls: bool):
        """
        Write a TAITherm file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surface_name_list : typing.List[str]
                Select surface.
            wall_function : bool
                'wall_function' child.
            htc_on_walls : bool
                'htc_on_walls' child.
        
        """

    def fieldview_unstruct(self, file_name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured combined file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def fieldview_unstruct_mesh(self, file_name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured mesh only file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def fieldview_unstruct_data(self, file_name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured results only file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def fieldview_unstruct_surfaces(self, option: str, file_name: str, surfaces: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured surface mesh, data.
        
        Parameters
        ----------
            option : str
                'option' child.
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                Select surface.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def ideas(self, file_name: str, surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write an IDEAS universal file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def nastran(self, file_name: str, bndry_threads: List[str], surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write a NASTRAN file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            bndry_threads : typing.List[str]
                Enter boundary zone name list.
            surfaces : typing.List[str]
                Select surface.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def patran_neutral(self, file_name: str, surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write a PATRAN neutral file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                Select surface.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def patran_nodal(self, file_name: str, surfaces: List[str], cell_func_domain_export: List[str]):
        """
        Write a PATRAN nodal results file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                'surfaces' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def tecplot(self, file_name: str, surfaces: List[str], cell_func_domain_export: List[str]):
        """
        Write a Tecplot+3DV format file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            surfaces : typing.List[str]
                Select surface.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

